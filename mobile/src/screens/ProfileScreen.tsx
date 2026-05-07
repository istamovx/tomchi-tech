import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  TouchableOpacity, Switch, ActivityIndicator, Linking,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import { sensorsApi, farmsApi, recommendationsApi } from '../services/api';

interface Stats {
  totalSensors:  number;
  onlineSensors: number;
  totalFarms:    number;
  avgSaving:     number;
}

export default function ProfileScreen() {
  const [stats, setStats]           = useState<Stats | null>(null);
  const [loading, setLoading]       = useState(true);
  const [notifs, setNotifs]         = useState(true);
  const [darkMode, setDarkMode]     = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchStats = useCallback(async () => {
    try {
      const [configs, farms, recs] = await Promise.all([
        sensorsApi.getConfigs(),
        farmsApi.getAll(),
        recommendationsApi.getAll(),
      ]);
      const online    = configs.filter(c => c.status === 'online').length;
      const totalSave = recs.reduce((s, r) => s + (r.water_saving_pct ?? 0), 0);
      const avgSaving = recs.length ? totalSave / recs.length : 0;
      setStats({
        totalSensors:  configs.length,
        onlineSensors: online,
        totalFarms:    farms.length,
        avgSaving,
      });
    } catch { /* silent */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchStats(); }, [fetchStats]);

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.content}>

        {/* App brand */}
        <View style={styles.brandCard}>
          <View style={styles.logoWrap}>
            <Text style={styles.logoEmoji}>💧</Text>
          </View>
          <Text style={styles.appName}>Tomchi Tech</Text>
          <Text style={styles.appTagline}>Aqlli sug'orish platformasi</Text>
          <View style={styles.versionBadge}>
            <Text style={styles.versionTxt}>v1.0.0</Text>
          </View>
        </View>

        {/* Stats */}
        {loading ? (
          <View style={styles.loadingWrap}>
            <ActivityIndicator size="small" color={colors.primary} />
          </View>
        ) : stats && (
          <View style={styles.statsGrid}>
            <StatBox icon="📡" label="Sensorlar" value={`${stats.onlineSensors}/${stats.totalSensors}`} sub="online" color={colors.primary} />
            <StatBox icon="🌾" label="Fermalar"  value={String(stats.totalFarms)}  sub="ro'yxatda" color="#7c3aed" />
            <StatBox icon="💧" label="Suv tejash" value={`${stats.avgSaving.toFixed(1)}%`} sub="o'rtacha" color={colors.success} />
            <StatBox icon="✅" label="Holat"      value={stats.onlineSensors === stats.totalSensors ? 'Yaxshi' : 'Muammo'} sub="tizim" color={stats.onlineSensors === stats.totalSensors ? colors.success : colors.danger} />
          </View>
        )}

        {/* Settings */}
        <SectionHeader title="Sozlamalar" />
        <View style={styles.settingsCard}>
          <SettingsRow
            icon="🔔"
            label="Bildirishnomalar"
            sub="Kritik alertlarni qabul qilish"
            right={<Switch value={notifs} onValueChange={setNotifs} trackColor={{ true: colors.primary }} thumbColor="#fff" />}
          />
          <View style={styles.sep} />
          <SettingsRow
            icon="🌙"
            label="Qorong'u rejim"
            sub="Tun uchun qulay ko'rinish"
            right={<Switch value={darkMode} onValueChange={setDarkMode} trackColor={{ true: colors.primary }} thumbColor="#fff" />}
          />
          <View style={styles.sep} />
          <SettingsRow
            icon="🔄"
            label="Avto yangilanish"
            sub="Har 30 soniyada ma'lumot yangilanadi"
            right={<Switch value={autoRefresh} onValueChange={setAutoRefresh} trackColor={{ true: colors.primary }} thumbColor="#fff" />}
          />
        </View>

        {/* System */}
        <SectionHeader title="Tizim" />
        <View style={styles.settingsCard}>
          <SettingsRow
            icon="🌐"
            label="API Server"
            sub="tomchi-tech-api.onrender.com"
            right={<View style={styles.onlineDot} />}
          />
          <View style={styles.sep} />
          <TouchableOpacity onPress={() => Linking.openURL('https://tomchi-tech-api.onrender.com/docs')}>
            <SettingsRow
              icon="📄"
              label="API Dokumentatsiya"
              sub="Swagger UI"
              right={<Text style={styles.linkArr}>›</Text>}
            />
          </TouchableOpacity>
        </View>

        {/* About */}
        <SectionHeader title="Haqida" />
        <View style={styles.settingsCard}>
          <SettingsRow icon="🏢" label="Ishlab chiqaruvchi" sub="Tomchi Tech Team" right={null} />
          <View style={styles.sep} />
          <SettingsRow icon="📋" label="Versiya" sub="1.0.0 (build 1)" right={null} />
          <View style={styles.sep} />
          <SettingsRow icon="📦" label="Platforma" sub="React Native + FastAPI" right={null} />
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerTxt}>© 2024 Tomchi Tech. Barcha huquqlar himoyalangan.</Text>
          <Text style={styles.footerSub}>O'zbekiston, Toshkent</Text>
        </View>

        <View style={{ height: 32 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

/* ── Sub-components ── */

function StatBox({ icon, label, value, sub, color }: { icon: string; label: string; value: string; sub: string; color: string }) {
  return (
    <View style={[statStyles.box, { borderTopColor: color, borderTopWidth: 3 }]}>
      <Text style={statStyles.icon}>{icon}</Text>
      <Text style={[statStyles.value, { color }]}>{value}</Text>
      <Text style={statStyles.label}>{label}</Text>
      <Text style={statStyles.sub}>{sub}</Text>
    </View>
  );
}

const statStyles = StyleSheet.create({
  box:   { flex: 1, backgroundColor: colors.bgWhite, borderRadius: radius.lg, padding: spacing.md, alignItems: 'center', gap: 2, ...shadow.xs, borderWidth: 1, borderColor: colors.stroke },
  icon:  { fontSize: 20, marginBottom: 2 },
  value: { ...typography.h3, fontWeight: '700' },
  label: { ...typography.labelSm, color: colors.textStrong },
  sub:   { ...typography.paraXs, color: colors.textSoft },
});

function SectionHeader({ title }: { title: string }) {
  return (
    <Text style={sectionStyles.title}>{title}</Text>
  );
}
const sectionStyles = StyleSheet.create({
  title: { ...typography.labelSm, color: colors.textSoft, textTransform: 'uppercase', letterSpacing: 0.8, paddingHorizontal: spacing.lg, paddingTop: spacing.lg, paddingBottom: spacing.xs },
});

function SettingsRow({ icon, label, sub, right }: { icon: string; label: string; sub: string; right: React.ReactNode }) {
  return (
    <View style={rowStyles.row}>
      <View style={rowStyles.iconWrap}>
        <Text style={rowStyles.icon}>{icon}</Text>
      </View>
      <View style={rowStyles.info}>
        <Text style={rowStyles.label}>{label}</Text>
        <Text style={rowStyles.sub}>{sub}</Text>
      </View>
      {right}
    </View>
  );
}
const rowStyles = StyleSheet.create({
  row:     { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, paddingVertical: spacing.md, gap: spacing.md },
  iconWrap:{ width: 36, height: 36, borderRadius: radius.md, backgroundColor: colors.bgSoft, justifyContent: 'center', alignItems: 'center' },
  icon:    { fontSize: 18 },
  info:    { flex: 1 },
  label:   { ...typography.labelMd, color: colors.textStrong },
  sub:     { ...typography.paraXs, color: colors.textSoft, marginTop: 1 },
});

/* ── Main styles ── */
const styles = StyleSheet.create({
  safe:        { flex: 1, backgroundColor: colors.bgWeak },
  content:     { paddingTop: spacing.md },

  brandCard:   { margin: spacing.lg, backgroundColor: colors.bgWhite, borderRadius: radius.lg, padding: spacing.xl, alignItems: 'center', borderWidth: 1, borderColor: colors.stroke, ...shadow.sm },
  logoWrap:    { width: 72, height: 72, borderRadius: radius.lg, backgroundColor: colors.primaryLight, justifyContent: 'center', alignItems: 'center', marginBottom: spacing.sm },
  logoEmoji:   { fontSize: 36 },
  appName:     { ...typography.h1, color: colors.textStrong, marginBottom: 4 },
  appTagline:  { ...typography.paraSm, color: colors.textSub },
  versionBadge:{ marginTop: spacing.sm, paddingHorizontal: spacing.md, paddingVertical: 4, backgroundColor: colors.bgSoft, borderRadius: radius.full, borderWidth: 1, borderColor: colors.stroke },
  versionTxt:  { ...typography.paraXs, color: colors.textSoft },

  loadingWrap: { height: 80, justifyContent: 'center', alignItems: 'center' },

  statsGrid:   { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: spacing.lg, gap: spacing.sm },

  settingsCard:{ marginHorizontal: spacing.lg, backgroundColor: colors.bgWhite, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.stroke, overflow: 'hidden', ...shadow.xs },
  sep:         { height: 1, backgroundColor: colors.stroke, marginLeft: spacing.lg + 36 + spacing.md },

  onlineDot:   { width: 8, height: 8, borderRadius: 4, backgroundColor: colors.success },
  linkArr:     { fontSize: 20, color: colors.textSoft },

  footer:      { alignItems: 'center', paddingTop: spacing.xl, gap: 4 },
  footerTxt:   { ...typography.paraXs, color: colors.textSoft, textAlign: 'center' },
  footerSub:   { ...typography.paraXs, color: colors.textSoft },
});
