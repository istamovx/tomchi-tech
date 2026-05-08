"""
Tomchi Tech — Integration Modules
==================================
Davlat tizimlari va to'lov tizimlari bilan integratsiya.

Foydalanish:
  1. cp .env.example .env
  2. .env faylini to'ldiring
  3. from integrations import myid, kadastr, agro, payme, click, uzum

Barcha classlar .enabled xususiyatiga ega —
kalitlar bo'lmasa, xatolik emas, shunchaki False qaytaradi.
"""

import os
import hmac
import hashlib
import json
import base64
import logging
from datetime import datetime
from typing import Optional

import httpx
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger("tomchi.integrations")


# ══════════════════════════════════════════════════════════════════
#  DAVLAT TIZIMLARI
# ══════════════════════════════════════════════════════════════════

class MyIDClient:
    """
    my.gov.uz — Elektron hukumat biometrik identifikatsiya tizimi
    Docs: https://developers.myid.uz
    Qo'llash: PINFL bo'yicha fuqaroni aniqlash, passport tekshirish
    """
    SANDBOX = "https://sandbox.myid.uz"
    PROD    = "https://api.myid.uz"

    def __init__(self):
        self.client_id     = os.getenv("MYID_CLIENT_ID", "")
        self.client_secret = os.getenv("MYID_CLIENT_SECRET", "")
        self.sandbox       = os.getenv("MYID_SANDBOX", "true").lower() == "true"
        self.base          = self.SANDBOX if self.sandbox else self.PROD

    @property
    def enabled(self) -> bool:
        return bool(self.client_id and self.client_secret)

    async def _token(self) -> str:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/oauth2/token", data={
                "grant_type":    "client_credentials",
                "client_id":     self.client_id,
                "client_secret": self.client_secret,
            })
            r.raise_for_status()
            return r.json()["access_token"]

    async def identify(self, pinfl: str) -> dict:
        """PINFL bo'yicha fuqaroni aniqlash"""
        if not self.enabled:
            return {"error": "MyID sozlanmagan — MYID_CLIENT_ID va MYID_CLIENT_SECRET kiriting"}
        token = await self._token()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{self.base}/api/v1/identification",
                params={"pinfl": pinfl},
                headers={"Authorization": f"Bearer {token}"},
            )
            r.raise_for_status()
            return r.json()

    async def verify_passport(self, serial: str, number: str, birth_date: str) -> dict:
        """Pasport ma'lumotlarini tekshirish"""
        if not self.enabled:
            return {"error": "MyID sozlanmagan"}
        token = await self._token()
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{self.base}/api/v1/verification/passport",
                json={"serial": serial, "number": number, "birth_date": birth_date},
                headers={"Authorization": f"Bearer {token}"},
            )
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "sandbox": self.sandbox, "base": self.base}


class KadastrClient:
    """
    kadastr.uz — O'zbekiston Davlat Yer Kadastr va GIS Agentligi
    Docs: https://api.kadastr.uz/docs
    Qo'llash: Yer uchastkasi ma'lumotlari, egasi, maydon, koordinatalar
    """
    def __init__(self):
        self.token = os.getenv("KADASTR_TOKEN", "")
        self.base  = os.getenv("KADASTR_BASE_URL", "https://api.kadastr.uz/v1")

    @property
    def enabled(self) -> bool:
        return bool(self.token)

    @property
    def _h(self) -> dict:
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    async def parcel(self, cadastral_number: str) -> dict:
        """Kadastr raqami bo'yicha yer uchastkasi"""
        if not self.enabled:
            return {"error": "Kadastr sozlanmagan — KADASTR_TOKEN kiriting"}
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/parcel/{cadastral_number}", headers=self._h)
            r.raise_for_status()
            return r.json()

    async def owner(self, cadastral_number: str) -> dict:
        """Yer uchastkasi egasi"""
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/parcel/{cadastral_number}/owner", headers=self._h)
            r.raise_for_status()
            return r.json()

    async def search_by_coords(self, lat: float, lon: float, radius_m: int = 100) -> dict:
        """Koordinatalar bo'yicha yer uchastkasini topish"""
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/parcel/search",
                params={"lat": lat, "lon": lon, "radius": radius_m}, headers=self._h)
            r.raise_for_status()
            return r.json()

    async def districts(self) -> list:
        """Viloyatlar va tumanlar ro'yxati"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/districts", headers=self._h)
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "base": self.base}


class AgroMinClient:
    """
    agro.uz — O'zbekiston Qishloq xo'jaligi vazirligi API
    Docs: https://api.agro.uz/docs
    Qo'llash: Fermerlar ro'yxati, ekin normatiflari, agro-meteorologiya
    """
    def __init__(self):
        self.token = os.getenv("AGRO_TOKEN", "")
        self.base  = os.getenv("AGRO_BASE_URL", "https://api.agro.uz/v1")

    @property
    def enabled(self) -> bool:
        return bool(self.token)

    @property
    def _h(self) -> dict:
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    async def farm_by_inn(self, inn: str) -> dict:
        """INN bo'yicha fermer xo'jaligi ma'lumotlari"""
        if not self.enabled:
            return {"error": "Agro vazirligi sozlanmagan — AGRO_TOKEN kiriting"}
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/farms/{inn}", headers=self._h)
            r.raise_for_status()
            return r.json()

    async def irrigation_norms(self, crop_type: str, region_id: int) -> dict:
        """Ekin turi va viloyat bo'yicha sug'orish normatiflari (m³/gektar)"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/norms/irrigation",
                params={"crop": crop_type, "region": region_id}, headers=self._h)
            r.raise_for_status()
            return r.json()

    async def agro_weather(self, lat: float, lon: float) -> dict:
        """Agro-meteorologik ma'lumot (yog'ingarchilik, temperatura, namlik)"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/weather",
                params={"lat": lat, "lon": lon}, headers=self._h)
            r.raise_for_status()
            return r.json()

    async def crop_calendar(self, crop_type: str, region_id: int) -> dict:
        """Ekin kalendari (ekish, parvarishlash, yig'im muddatlari)"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/calendar/{crop_type}",
                params={"region": region_id}, headers=self._h)
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "base": self.base}


class EGovClient:
    """
    egov.uz — O'zbekiston Elektron Hukumat portali
    Docs: https://api.egov.uz/docs
    Qo'llash: Davlat xizmatlari, hujjatlar tekshiruv
    """
    def __init__(self):
        self.api_key = os.getenv("EGOV_API_KEY", "")
        self.base    = os.getenv("EGOV_BASE_URL", "https://api.egov.uz/v1")

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    @property
    def _h(self) -> dict:
        return {"X-API-Key": self.api_key, "Accept": "application/json"}

    async def entity_info(self, inn: str) -> dict:
        """Yuridik shaxs ma'lumotlari (INN bo'yicha)"""
        if not self.enabled:
            return {"error": "E-hukumat sozlanmagan — EGOV_API_KEY kiriting"}
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/entity/{inn}", headers=self._h)
            r.raise_for_status()
            return r.json()

    async def service_status(self, application_id: str) -> dict:
        """Ariza holati"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/applications/{application_id}", headers=self._h)
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "base": self.base}


class SoliqClient:
    """
    soliq.uz — O'zbekiston Davlat Soliq Qo'mitasi
    Docs: https://api.soliq.uz/docs
    Qo'llash: Soliq to'lovchi tekshiruv, hisob-faktura
    """
    def __init__(self):
        self.tin   = os.getenv("SOLIQ_TIN", "")
        self.token = os.getenv("SOLIQ_TOKEN", "")
        self.base  = "https://api.soliq.uz/v1"

    @property
    def enabled(self) -> bool:
        return bool(self.tin and self.token)

    async def taxpayer(self, inn: str) -> dict:
        """INN bo'yicha soliq to'lovchi ma'lumoti"""
        if not self.enabled:
            return {"error": "Soliq qo'mitasi sozlanmagan"}
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/taxpayer/{inn}",
                headers={"Authorization": f"Bearer {self.token}"})
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled}


# ══════════════════════════════════════════════════════════════════
#  TO'LOV TIZIMLARI
# ══════════════════════════════════════════════════════════════════

class PaymeClient:
    """
    payme.uz — O'zbekistondagi #1 to'lov tizimi
    Docs: https://developer.help.paycom.uz
    Webhook: POST /webhook/payme
    """
    SANDBOX = "https://checkout.test.paycom.uz"
    PROD    = "https://checkout.paycom.uz"
    API     = "https://checkout.paycom.uz/api"

    def __init__(self):
        self.merchant_id = os.getenv("PAYME_MERCHANT_ID", "")
        self.key         = os.getenv("PAYME_SECRET_KEY", "")
        self.test_mode   = os.getenv("PAYME_TEST_MODE", "true").lower() == "true"

    @property
    def enabled(self) -> bool:
        return bool(self.merchant_id and self.key)

    def checkout_url(self, amount_uzs: float, order_id: str,
                     description: str = "", return_url: str = "") -> str:
        """To'lov sahifasi URL (amount so'mda, tiyin avtomatik)"""
        payload = base64.b64encode(json.dumps({
            "m": self.merchant_id,
            "ac": {"order_id": order_id},
            "a": int(amount_uzs * 100),   # tiyin
            "l": "uz",
            "d": description,
            "c": return_url,
        }).encode()).decode()
        base = self.SANDBOX if self.test_mode else self.PROD
        return f"{base}/{payload}"

    def verify_webhook(self, auth_header: str) -> bool:
        """POST /webhook/payme — Authorization headerini tekshirish"""
        try:
            encoded = auth_header.replace("Basic ", "")
            decoded = base64.b64decode(encoded).decode()
            _, received = decoded.split(":", 1)
            return hmac.compare_digest(received, self.key)
        except Exception:
            return False

    async def check_payment(self, transaction_id: str) -> dict:
        """To'lov holatini so'rash"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(self.API,
                json={"id": 1, "method": "receipts.get",
                      "params": {"id": transaction_id}},
                auth=(self.merchant_id, self.key))
            r.raise_for_status()
            return r.json()

    async def cancel_payment(self, transaction_id: str, reason: int = 4) -> dict:
        """To'lovni bekor qilish (reason: 1=stock, 2=delivery, 3=other, 4=other)"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(self.API,
                json={"id": 1, "method": "receipts.cancel",
                      "params": {"id": transaction_id, "reason": reason}},
                auth=(self.merchant_id, self.key))
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "test_mode": self.test_mode}


class ClickClient:
    """
    click.uz — O'zbekistondagi ikkinchi katta to'lov tizimi
    Docs: https://docs.click.uz
    Webhook: POST /webhook/click  (prepare + complete)
    """
    CHECKOUT = "https://my.click.uz/services/pay"
    API      = "https://api.click.uz/v2/merchant"

    def __init__(self):
        self.merchant_id = os.getenv("CLICK_MERCHANT_ID", "")
        self.service_id  = os.getenv("CLICK_SERVICE_ID", "")
        self.secret_key  = os.getenv("CLICK_SECRET_KEY", "")
        self.test_mode   = os.getenv("CLICK_TEST_MODE", "true").lower() == "true"

    @property
    def enabled(self) -> bool:
        return bool(self.merchant_id and self.service_id and self.secret_key)

    def checkout_url(self, amount: float, order_id: str, return_url: str = "") -> str:
        """Click to'lov sahifasi URL"""
        from urllib.parse import urlencode
        params = {
            "service_id":        self.service_id,
            "merchant_id":       self.merchant_id,
            "amount":            amount,
            "transaction_param": order_id,
            "return_url":        return_url,
            "card_type":         "uzcard",
        }
        return f"{self.CHECKOUT}?{urlencode(params)}"

    def _auth_header(self) -> str:
        sign_time = str(int(datetime.now().timestamp()))
        sign = hashlib.md5(f"{sign_time}{self.secret_key}".encode()).hexdigest()
        return f"{self.merchant_id}:{sign_time}:{sign}"

    def verify_webhook(self, sign_time: str, sign_string: str) -> bool:
        """Click webhook imzosini tekshirish"""
        expected = hashlib.md5(f"{sign_time}{self.secret_key}".encode()).hexdigest()
        return hmac.compare_digest(expected, sign_string)

    async def check_payment(self, payment_id: str) -> dict:
        """To'lov holati"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{self.API}/payment/status/{self.service_id}/{payment_id}",
                headers={"Auth": self._auth_header()})
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "test_mode": self.test_mode}


class UzumBankClient:
    """
    uzumbank.uz — Yangi avlod to'lov tizimi
    Docs: https://developers.uzumbank.uz
    Webhook: POST /webhook/uzum
    """
    SANDBOX = "https://sandbox-api.uzumbank.uz"
    PROD    = "https://api.uzumbank.uz"

    def __init__(self):
        self.shop_id   = os.getenv("UZUM_SHOP_ID", "")
        self.token     = os.getenv("UZUM_TOKEN", "")
        self.test_mode = os.getenv("UZUM_TEST_MODE", "true").lower() == "true"
        self.base      = self.SANDBOX if self.test_mode else self.PROD

    @property
    def enabled(self) -> bool:
        return bool(self.shop_id and self.token)

    @property
    def _h(self) -> dict:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    async def create_order(self, amount_uzs: float, order_id: str,
                           description: str = "") -> dict:
        """To'lov buyurtmasi yaratish"""
        if not self.enabled:
            return {"error": "Uzum Bank sozlanmagan"}
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/v1/checkout/create", json={
                "shopId":      self.shop_id,
                "amount":      int(amount_uzs * 100),
                "orderId":     order_id,
                "description": description,
                "currency":    "UZS",
            }, headers=self._h)
            r.raise_for_status()
            return r.json()

    async def check_status(self, order_id: str) -> dict:
        """To'lov holati"""
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{self.base}/v1/checkout/{order_id}", headers=self._h)
            r.raise_for_status()
            return r.json()

    async def refund(self, order_id: str, amount_uzs: Optional[float] = None) -> dict:
        """To'lovni qaytarish (to'liq yoki qisman)"""
        body: dict = {"orderId": order_id}
        if amount_uzs:
            body["amount"] = int(amount_uzs * 100)
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/v1/checkout/refund", json=body, headers=self._h)
            r.raise_for_status()
            return r.json()

    def status(self) -> dict:
        return {"enabled": self.enabled, "test_mode": self.test_mode}


# ══════════════════════════════════════════════════════════════════
#  SINGLETON INSTANCES
#  from integrations import myid, kadastr, agro, payme, click, uzum
# ══════════════════════════════════════════════════════════════════

myid    = MyIDClient()
kadastr = KadastrClient()
agro    = AgroMinClient()
egov    = EGovClient()
soliq   = SoliqClient()
payme   = PaymeClient()
click   = ClickClient()
uzum    = UzumBankClient()


def all_statuses() -> dict:
    """Barcha integratsiyalar holatini bir qaramda ko'rish"""
    return {
        "gov": {
            "myid":    myid.status(),
            "kadastr": kadastr.status(),
            "agro":    agro.status(),
            "egov":    egov.status(),
            "soliq":   soliq.status(),
        },
        "payment": {
            "payme": payme.status(),
            "click": click.status(),
            "uzum":  uzum.status(),
        }
    }


if __name__ == "__main__":
    import pprint
    print("=== Tomchi Tech — Integration Status ===")
    pprint.pprint(all_statuses())
