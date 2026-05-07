import React, { useEffect, useState } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  ActivityIndicator, TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import { sensorsApi, recommendationsApi } from '../services/api';
import type { SensorReading, SensorConfig, Recommendation } from '../services/api';

const ACTION_CONFIG = {
  IRRIGATE_NOW:   { label: 'Darhol sug\'or!', color: colors.danger,  bg: colors.dangerBg,  icon: '🚨' },
  IRRIGATE_SOON:  { label: 'Tez sug\'or',     color: colors.warning, bg: colors.warningBg, icon: '⚠️' },
  STOP_IRRIGATION:{ label: 'Sug\'orishni to\'xtat', color: colors.neutral, bg: colors.neutralBg, icon: '🛑' },
  NO_ACTION:      { label: 'Yaxshi holat',    color: colors.success, bg: colors.successBg, icon: '✅' },
};

export default function SensorDetailScreen({ route, navigation }: any) {
  const { sensorId } = route.params;
  const [reading, setReading]         = useState<SensorReading | null>(null);
  const [config, setConfig]           = useState<SensorConfig | null>(null);
  const [rec, setRec]                 = useState<Recommendation | null>(null);
  const [history, setHistory]         = useState<SensorReading[]>([]);
  const [loading, setLoading]         = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const [r, configs, recommendation, hist] = await Promise.all([
          sensorsApi.getOne(sensorId),
          sensorsApi.getConfigs(),
          recommendationsApi.getOne(sensorId),
          sensorsApi.getHistory(sensorId, 12),
        ]);
        setReading(r);
        setConfig(configs.find(c => c.sensor_id === sensorId) ?? null);
        setRec(recommendation);
        setHistory(hist);
      } catch { /* handle */ }
      finally { setLoading(false); }
    })();
  }, [sensorId]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  if (!reading || !rec) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>Ma'lumot topilmadi</Text>
      </View>
    );
  }

  const actionCfg = ACTION_CONFIG[rec.action] ?? ACTION_CONFIG.NO_ACTION;
  const maxMoisture = Math.max(...history.map(h => h.soil_moisture), 1);

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      {/* Nav header */}
      <View style={styles.navHeader}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <Text style={styles.backIcon}>←</Text>
        </TouchableOpacity>
        <Text style={styles.navTitle}>Dala tahlili</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView style={styles.scroll} contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
        {/* Title */}
        <Text style={styles.sensorTitle}>{sensorId} · {config?.crop_type ?? '—'}</Text>
        <Text style={styles.sensorSub}>
          📍 {config?.field_area_ha} ga · {config?.farm_id}
        </Text>

        {/* Score card */}
        <View style={[styles.scoreCard, { backgroundColor: actionCfg.bg, borderColor: actionCfg.color + '40' }]}>
          <View style={styles.scoreLeft}>
            <Text style={[styles.scoreLabel, { color: actionCfg.color }]}>Namlik skori</Text>
            <View style={styles.scoreNumRow}>
              <Text style={[styles.scoreNum, { color: colors.textStrong }]}>
                {reading.soil_moisture.toFixed(1)}
              </Text>
              <Text style={[styles.scoreUnit, { color: actionCfg.color }]}>% {actionCfg.icon}</Text>
            </View>
          </View>
          <View style={[styles.actionBadge, { backgroundColor: actionCfg.color }]}>
            <Text style={styles.actionBadgeText}>{actionCfg.label}</Text>
          </View>
        </View>

        {/* Metric cards */}
        <View style={styles.metricsRow}>
          <View style={styles.metricCard}>
            <Text style={styles.metricIcon}>🌡</Text>
            <Text style={styles.metricLabel}>Harorat</Text>
            <Text style={styles.metricVal}>{reading.temperature.toFixed(1)}°C</Text>
          </View>
          <View style={styles.metricCard}>
            <Text style={styles.metricIcon}>💧</Text>
            <Text style={styles.metricLabel}>Havo namligi</Text>
            <Text style={styles.metricVal}>{reading.humidity.toFixed(0)}%</Text>
          </View>
          <View style={styles.metricCard}>
            <Text style={styles.metricIcon}>♻️</Text>
            <Text style={styles.metricLabel}>Tejash</Text>
            <Text style={[styles.metricVal, { color: colors.primary }]}>
              {rec.water_saving_pct.toFixed(1)}%
            </Text>
          </View>
        </View>

        {/* Tavsiya */}
        <View style={styles.recCard}>
          <Text style={styles.recTitle}>💡 Tavsiya</Text>
          <Text style={styles.recMessage}>{rec.message}</Text>
          <View style={styles.recRow}>
            {rec.water_needed_liters > 0 && (
              <View style={styles.recChip}>
                <Text style={styles.recChipText}>💧 {rec.water_needed_liters.toLocaleString()} L kerak</Text>
              </View>
            )}
            <View style={styles.recChip}>
              <Text style={styles.recChipText}>
                Optimal: {rec.optimal_range.min}–{rec.optimal_range.max}%
              </Text>
            </View>
          </View>
        </View>

        {/* History chart */}
        <View style={styles.chartCard}>
          <Text style={styles.chartTitle}>Namlik tarixi (12 soat)</Text>
          <View style={styles.chartArea}>
            {history.slice(-24).map((h, i) => {
              const heightPct = (h.soil_moisture / 100) * 60;
              const isLow = h.soil_moisture < (config?.irrigation_threshold ?? 45);
              return (
                <View key={i} style={styles.barCol}>
                  <View style={[
                    styles.histBar,
                    {
                      height: heightPct,
                      backgroundColor: isLow ? colors.danger : colors.primary,
                      opacity: 0.7 + (i / history.length) * 0.3,
                    },
                  ]} />
                </View>
              );
            })}
          </View>
          <View style={styles.chartLegend}>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, { backgroundColor: colors.primary }]} />
              <Text style={styles.legendText}>Normal</Text>
            </View>
            <View style={styles.legendItem}>
              <View style={[styles.legendDot, { backgroundColor: colors.danger }]} />
              <Text style={styles.legendText}>Past (sug'or)</Text>
            </View>
          </View>
        </View>

        {/* Water comparison */}
        <View style={styles.waterCard}>
          <Text style={styles.recTitle}>💦 Suv sarfi taqqoslash</Text>
          <View style={styles.waterRow}>
            <View style={styles.waterItem}>
              <Text style={styles.waterLabel}>An'anaviy usul</Text>
              <Text style={[styles.waterVal, { color: colors.danger }]}>
                {rec.traditional_method_liters.toLocaleString()} L
              </Text>
            </View>
            <Text style={styles.waterVs}>vs</Text>
            <View style={styles.waterItem}>
              <Text style={styles.waterLabel}>Tomchi Tech</Text>
              <Text style={[styles.waterVal, { color: colors.primary }]}>
                {rec.water_needed_liters.toLocaleString()} L
              </Text>
            </View>
          </View>
          <View style={styles.savingBanner}>
            <Text style={styles.savingText}>
              🎉 {rec.water_saving_pct.toFixed(1)}% tejash — bu {(rec.traditional_method_liters - rec.water_needed_liters).toLocaleString()} L kam!
            </Text>
          </View>
        </View>

        <View style={{ height: 32 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:        { flex: 1, backgroundColor: colors.bgWeak },
  scroll:      { flex: 1 },
  container:   { padding: spacing.lg, gap: spacing.md },
  center:      { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.bgWeak },
  errorText:   { ...typography.paraSm, color: colors.textSoft },
  navHeader:   {
    flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between',
    padding: spacing.md, backgroundColor: colors.bgWhite,
    borderBottomWidth: 1, borderColor: colors.stroke,
  },
  backBtn:     { width: 40, height: 40, alignItems: 'center', justifyContent: 'center' },
  backIcon:    { fontSize: 22, color: colors.textStrong },
  navTitle:    { ...typography.labelMd, color: colors.textSoft },
  sensorTitle: { ...typography.h2, color: colors.textStrong },
  sensorSub:   { ...typography.paraXs, color: colors.textSoft, marginTop: 2 },
  scoreCard:   {
    borderRadius: radius.lg, padding: spacing.lg,
    flexDirection: 'row', alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
  },
  scoreLeft:   { gap: 4 },
  scoreLabel:  { fontSize: 11, fontWeight: '700', textTransform: 'uppercase', letterSpacing: 0.5 },
  scoreNumRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 4 },
  scoreNum:    { fontSize: 40, fontWeight: '800', lineHeight: 44 },
  scoreUnit:   { fontSize: 16, fontWeight: '600', marginBottom: 4 },
  actionBadge: { borderRadius: radius.md, paddingHorizontal: 12, paddingVertical: 8 },
  actionBadgeText: { color: 'white', fontWeight: '700', fontSize: 12 },
  metricsRow:  { flexDirection: 'row', gap: spacing.sm },
  metricCard:  {
    flex: 1, backgroundColor: colors.bgWhite,
    borderRadius: radius.lg, padding: spacing.md,
    borderWidth: 1, borderColor: colors.stroke,
    alignItems: 'flex-start', gap: 4, ...shadow.xs,
  },
  metricIcon:  { fontSize: 18 },
  metricLabel: { ...typography.paraXs, color: colors.textSoft },
  metricVal:   { ...typography.labelMd, color: colors.textStrong },
  recCard:     {
    backgroundColor: colors.bgWhite, borderRadius: radius.lg,
    padding: spacing.md, borderWidth: 1, borderColor: colors.stroke,
    gap: 8, ...shadow.xs,
  },
  recTitle:    { ...typography.labelSm, color: colors.textStrong },
  recMessage:  { ...typography.paraSm, color: colors.textSub, lineHeight: 20 },
  recRow:      { flexDirection: 'row', gap: spacing.sm, flexWrap: 'wrap' },
  recChip:     {
    backgroundColor: colors.bgWeak, borderRadius: radius.sm,
    paddingHorizontal: 8, paddingVertical: 3,
  },
  recChipText: { fontSize: 11, color: colors.textSub },
  chartCard:   {
    backgroundColor: colors.bgWhite, borderRadius: radius.lg,
    padding: spacing.md, borderWidth: 1, borderColor: colors.stroke, ...shadow.xs,
  },
  chartTitle:  { ...typography.labelSm, color: colors.textStrong, marginBottom: spacing.sm },
  chartArea:   {
    flexDirection: 'row', alignItems: 'flex-end',
    height: 70, gap: 2,
  },
  barCol:      { flex: 1, alignItems: 'center', justifyContent: 'flex-end', height: '100%' },
  histBar:     { width: '100%', borderRadius: 2, minHeight: 3 },
  chartLegend: { flexDirection: 'row', gap: spacing.md, marginTop: spacing.sm },
  legendItem:  { flexDirection: 'row', alignItems: 'center', gap: 5 },
  legendDot:   { width: 8, height: 8, borderRadius: radius.full },
  legendText:  { ...typography.paraXs, color: colors.textSoft },
  waterCard:   {
    backgroundColor: colors.bgWhite, borderRadius: radius.lg,
    padding: spacing.md, borderWidth: 1, borderColor: colors.stroke,
    gap: spacing.sm, ...shadow.xs,
  },
  waterRow:    {
    flexDirection: 'row', alignItems: 'center',
    justifyContent: 'space-around', marginTop: 4,
  },
  waterItem:   { alignItems: 'center', gap: 4 },
  waterLabel:  { ...typography.paraXs, color: colors.textSoft },
  waterVal:    { ...typography.h3 },
  waterVs:     { ...typography.paraXs, color: colors.textSoft },
  savingBanner:{
    backgroundColor: colors.primaryLight, borderRadius: radius.md,
    padding: spacing.sm,
  },
  savingText:  { ...typography.paraSm, color: colors.primary, fontWeight: '500', textAlign: 'center' },
});
