import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  RefreshControl, ActivityIndicator, TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import { sensorsApi, recommendationsApi, alertsApi } from '../services/api';
import type { SensorReading, SensorConfig, Recommendation, Alert } from '../services/api';
import SensorCard from '../components/SensorCard';

export default function DashboardScreen({ navigation }: any) {
  const [readings, setReadings]             = useState<SensorReading[]>([]);
  const [configs, setConfigs]               = useState<SensorConfig[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [alerts, setAlerts]                 = useState<Alert[]>([]);
  const [loading, setLoading]               = useState(true);
  const [refreshing, setRefreshing]         = useState(false);
  const [error, setError]                   = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setError(null);
      const [r, c, rec, al] = await Promise.all([
        sensorsApi.getAll(),
        sensorsApi.getConfigs(),
        recommendationsApi.getAll(),
        alertsApi.getAll(),
      ]);
      setReadings(r);
      setConfigs(c);
      setRecommendations(rec);
      setAlerts(al.alerts);
    } catch (e: any) {
      setError('Server bilan ulanishda xato. Qayta urinib ko\'ring.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const onRefresh = () => { setRefreshing(true); fetchData(); };

  const getConfig = (sensor_id: string) =>
    configs.find(c => c.sensor_id === sensor_id);

  const onlineCount  = configs.filter(c => c.status === 'online').length;
  const criticalRecs = recommendations.filter(r => r.action === 'IRRIGATE_NOW');
  const soonRecs     = recommendations.filter(r => r.action === 'IRRIGATE_SOON');
  const totalSaving  = recommendations.reduce((s, r) => s + (r.water_saving_pct ?? 0), 0);
  const avgSaving    = recommendations.length ? (totalSaving / recommendations.length).toFixed(1) : '—';

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Sensorlar yuklanmoqda...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.container}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Assalomu alaykum 👋</Text>
            <Text style={styles.title}>Dashboard</Text>
          </View>
          <TouchableOpacity
            style={styles.alertBell}
            onPress={() => navigation.navigate('Alerts')}
          >
            <Text style={styles.bellIcon}>🔔</Text>
            {alerts.length > 0 && (
              <View style={styles.bellBadge}>
                <Text style={styles.bellBadgeText}>{alerts.length}</Text>
              </View>
            )}
          </TouchableOpacity>
        </View>

        {/* Error */}
        {error && (
          <View style={styles.errorBanner}>
            <Text style={styles.errorText}>⚠️ {error}</Text>
          </View>
        )}

        {/* Stats row */}
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.statsScroll}>
          <View style={styles.statsRow}>
            <View style={[styles.statCard, { borderLeftColor: colors.primary }]}>
              <Text style={styles.statNum}>{onlineCount}/6</Text>
              <Text style={styles.statLabel}>Online sensor</Text>
            </View>
            <View style={[styles.statCard, { borderLeftColor: colors.danger }]}>
              <Text style={[styles.statNum, { color: colors.danger }]}>{criticalRecs.length}</Text>
              <Text style={styles.statLabel}>Kritik</Text>
            </View>
            <View style={[styles.statCard, { borderLeftColor: colors.warning }]}>
              <Text style={[styles.statNum, { color: colors.warning }]}>{soonRecs.length}</Text>
              <Text style={styles.statLabel}>Tez sug'or</Text>
            </View>
            <View style={[styles.statCard, { borderLeftColor: colors.success }]}>
              <Text style={[styles.statNum, { color: colors.success }]}>{avgSaving}%</Text>
              <Text style={styles.statLabel}>O'rtacha tejash</Text>
            </View>
          </View>
        </ScrollView>

        {/* Kritik tavsiyalar */}
        {criticalRecs.length > 0 && (
          <View style={styles.section}>
            <View style={styles.sectionHeader}>
              <Text style={styles.sectionTitle}>🚨 Darhol harakat kerak</Text>
            </View>
            {criticalRecs.map(rec => (
              <TouchableOpacity
                key={rec.sensor_id}
                style={styles.criticalCard}
                onPress={() => navigation.navigate('SensorDetail', { sensorId: rec.sensor_id })}
                activeOpacity={0.8}
              >
                <View style={styles.criticalTop}>
                  <Text style={styles.criticalId}>{rec.sensor_id} · {rec.crop_type}</Text>
                  <View style={styles.criticalBadge}>
                    <Text style={styles.criticalBadgeText}>IRRIGATE_NOW</Text>
                  </View>
                </View>
                <Text style={styles.criticalMsg}>{rec.message}</Text>
                <View style={styles.criticalRow}>
                  <Text style={styles.criticalChip}>💧 {rec.water_needed_liters.toLocaleString()} L kerak</Text>
                  <Text style={styles.criticalChip}>📉 {rec.current_moisture.toFixed(1)}% namlik</Text>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}

        {/* Sensorlar */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>📡 Barcha sensorlar</Text>
            <TouchableOpacity onPress={() => navigation.navigate('Sensors')}>
              <Text style={styles.seeAll}>Barchasi ›</Text>
            </TouchableOpacity>
          </View>
          {readings.map(reading => (
            <SensorCard
              key={reading.sensor_id}
              reading={reading}
              config={getConfig(reading.sensor_id)}
              onPress={() => navigation.navigate('SensorDetail', { sensorId: reading.sensor_id })}
            />
          ))}
        </View>

        <View style={{ height: 20 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bgWeak },
  scroll: { flex: 1 },
  container: { padding: spacing.lg },
  center: {
    flex: 1, alignItems: 'center', justifyContent: 'center',
    backgroundColor: colors.bgWeak,
  },
  loadingText: {
    ...typography.paraSm,
    color: colors.textSoft,
    marginTop: spacing.md,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: spacing.lg,
  },
  greeting: {
    ...typography.paraXs,
    color: colors.textSoft,
    marginBottom: 2,
  },
  title: {
    ...typography.h2,
    color: colors.textStrong,
  },
  alertBell: {
    width: 44, height: 44,
    backgroundColor: colors.bgWhite,
    borderRadius: radius.lg,
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 1, borderColor: colors.stroke,
    ...shadow.xs,
    position: 'relative',
  },
  bellIcon: { fontSize: 20 },
  bellBadge: {
    position: 'absolute', top: 8, right: 8,
    width: 16, height: 16,
    backgroundColor: colors.danger,
    borderRadius: radius.full,
    alignItems: 'center', justifyContent: 'center',
    borderWidth: 2, borderColor: colors.bgWhite,
  },
  bellBadgeText: { fontSize: 9, color: 'white', fontWeight: '700' },
  errorBanner: {
    backgroundColor: colors.dangerBg,
    borderRadius: radius.md,
    padding: spacing.md,
    marginBottom: spacing.md,
  },
  errorText: {
    ...typography.paraSm,
    color: colors.danger,
  },
  statsScroll: { marginBottom: spacing.lg },
  statsRow: { flexDirection: 'row', gap: spacing.sm, paddingRight: spacing.lg },
  statCard: {
    backgroundColor: colors.bgWhite,
    borderRadius: radius.lg,
    padding: spacing.md,
    minWidth: 100,
    borderLeftWidth: 3,
    borderWidth: 1,
    borderColor: colors.stroke,
    ...shadow.xs,
  },
  statNum: {
    ...typography.h3,
    color: colors.textStrong,
  },
  statLabel: {
    ...typography.paraXs,
    color: colors.textSoft,
    marginTop: 2,
  },
  section: { marginBottom: spacing.lg },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  sectionTitle: {
    ...typography.labelMd,
    color: colors.textStrong,
  },
  seeAll: {
    ...typography.paraSm,
    color: colors.primary,
    fontWeight: '500',
  },
  criticalCard: {
    backgroundColor: colors.dangerBg,
    borderRadius: radius.lg,
    padding: spacing.md,
    marginBottom: spacing.sm,
    borderWidth: 1,
    borderColor: '#fca5a5',
    gap: 6,
  },
  criticalTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  criticalId: {
    ...typography.labelSm,
    color: colors.danger,
  },
  criticalBadge: {
    backgroundColor: colors.danger,
    borderRadius: radius.full,
    paddingHorizontal: 8, paddingVertical: 2,
  },
  criticalBadgeText: {
    fontSize: 10, color: 'white', fontWeight: '700',
  },
  criticalMsg: {
    ...typography.paraSm,
    color: '#7f1d1d',
  },
  criticalRow: {
    flexDirection: 'row', gap: spacing.sm, marginTop: 2,
  },
  criticalChip: {
    fontSize: 11, color: '#991b1b',
    backgroundColor: '#fee2e2',
    borderRadius: radius.sm,
    paddingHorizontal: 7, paddingVertical: 2,
  },
});
