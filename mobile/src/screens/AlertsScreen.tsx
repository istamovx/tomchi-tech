import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  RefreshControl, ActivityIndicator, TouchableOpacity,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import { alertsApi } from '../services/api';
import type { Alert } from '../services/api';

const SEV_CONFIG = {
  critical: { color: colors.danger,  bg: colors.dangerBg,  icon: '🚨', label: 'Kritik' },
  error:    { color: '#dc2626',      bg: '#fee2e2',         icon: '❌', label: 'Xato'   },
  warning:  { color: colors.warning, bg: colors.warningBg, icon: '⚠️', label: 'Diqqat' },
};

export default function AlertsScreen({ navigation }: any) {
  const [alerts, setAlerts]       = useState<Alert[]>([]);
  const [loading, setLoading]     = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter]       = useState<'all' | 'critical' | 'warning'>('all');

  const fetchAlerts = useCallback(async () => {
    try {
      const data = await alertsApi.getAll();
      setAlerts(data.alerts);
    } catch { /* handle */ }
    finally { setLoading(false); setRefreshing(false); }
  }, []);

  useEffect(() => { fetchAlerts(); }, [fetchAlerts]);

  const filtered = filter === 'all'
    ? alerts
    : alerts.filter(a => a.severity === filter);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <View style={styles.header}>
        <Text style={styles.title}>🔔 Ogohlantirishlar</Text>
        <View style={styles.countBadge}>
          <Text style={styles.countText}>{alerts.length}</Text>
        </View>
      </View>

      {/* Filter tabs */}
      <View style={styles.tabs}>
        {(['all', 'critical', 'warning'] as const).map(tab => (
          <TouchableOpacity
            key={tab}
            style={[styles.tab, filter === tab && styles.tabActive]}
            onPress={() => setFilter(tab)}
          >
            <Text style={[styles.tabText, filter === tab && styles.tabTextActive]}>
              {tab === 'all' ? 'Barchasi' : tab === 'critical' ? 'Kritik' : 'Diqqat'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.container}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); fetchAlerts(); }} tintColor={colors.primary} />}
        showsVerticalScrollIndicator={false}
      >
        {filtered.length === 0 ? (
          <View style={styles.empty}>
            <Text style={styles.emptyIcon}>✅</Text>
            <Text style={styles.emptyTitle}>Ogohlantirishlar yo'q</Text>
            <Text style={styles.emptyText}>Barcha sensorlar yaxshi ishlayapti</Text>
          </View>
        ) : (
          filtered.map((alert, i) => {
            const cfg = SEV_CONFIG[alert.severity] ?? SEV_CONFIG.warning;
            return (
              <TouchableOpacity
                key={i}
                style={[styles.alertCard, { borderLeftColor: cfg.color }]}
                onPress={() => navigation.navigate('SensorDetail', { sensorId: alert.sensor_id })}
                activeOpacity={0.75}
              >
                <View style={styles.alertTop}>
                  <Text style={styles.alertIcon}>{cfg.icon}</Text>
                  <View style={styles.alertInfo}>
                    <Text style={styles.alertTitle}>{alert.message}</Text>
                    <Text style={styles.alertMeta}>
                      {alert.sensor_id} · {alert.farm_id}
                      {alert.value != null ? ` · ${alert.value.toFixed(1)}` : ''}
                    </Text>
                  </View>
                  <View style={[styles.sevBadge, { backgroundColor: cfg.bg }]}>
                    <Text style={[styles.sevText, { color: cfg.color }]}>{cfg.label}</Text>
                  </View>
                </View>
                <View style={styles.alertFooter}>
                  <Text style={styles.alertType}>{alert.type}</Text>
                  <Text style={styles.alertTime}>
                    {new Date(alert.at).toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })}
                  </Text>
                </View>
              </TouchableOpacity>
            );
          })
        )}
        <View style={{ height: 20 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:     { flex: 1, backgroundColor: colors.bgWeak },
  center:   { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.bgWeak },
  header:   {
    flexDirection: 'row', alignItems: 'center', gap: spacing.sm,
    padding: spacing.lg, paddingBottom: spacing.md,
    backgroundColor: colors.bgWhite, borderBottomWidth: 1, borderColor: colors.stroke,
  },
  title:    { ...typography.h3, color: colors.textStrong, flex: 1 },
  countBadge: {
    backgroundColor: colors.danger, borderRadius: radius.full,
    paddingHorizontal: 8, paddingVertical: 3,
  },
  countText: { fontSize: 12, fontWeight: '700', color: 'white' },
  tabs:     {
    flexDirection: 'row',
    backgroundColor: colors.bgWhite,
    borderBottomWidth: 1, borderColor: colors.stroke,
    paddingHorizontal: spacing.lg,
  },
  tab:      { paddingVertical: 12, paddingHorizontal: 4, marginRight: spacing.lg, borderBottomWidth: 2, borderColor: 'transparent' },
  tabActive:{ borderBottomColor: colors.textStrong },
  tabText:  { ...typography.labelSm, color: colors.textSoft },
  tabTextActive: { color: colors.textStrong },
  scroll:   { flex: 1 },
  container:{ padding: spacing.lg, gap: spacing.sm },
  empty:    { alignItems: 'center', paddingTop: 60, gap: spacing.sm },
  emptyIcon:{ fontSize: 48 },
  emptyTitle: { ...typography.labelLg, color: colors.textStrong },
  emptyText:  { ...typography.paraSm, color: colors.textSoft },
  alertCard:  {
    backgroundColor: colors.bgWhite,
    borderRadius: radius.lg,
    borderWidth: 1, borderColor: colors.stroke,
    borderLeftWidth: 4,
    padding: spacing.md,
    gap: spacing.sm,
    ...shadow.xs,
  },
  alertTop:  { flexDirection: 'row', alignItems: 'flex-start', gap: spacing.sm },
  alertIcon: { fontSize: 20, marginTop: 1 },
  alertInfo: { flex: 1, gap: 3 },
  alertTitle:{ ...typography.labelSm, color: colors.textStrong },
  alertMeta: { ...typography.paraXs, color: colors.textSoft },
  sevBadge:  { borderRadius: radius.full, paddingHorizontal: 8, paddingVertical: 3 },
  sevText:   { fontSize: 11, fontWeight: '600' },
  alertFooter:{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' },
  alertType: {
    fontSize: 10, fontWeight: '700', color: colors.textSoft,
    backgroundColor: colors.bgWeak, borderRadius: radius.sm,
    paddingHorizontal: 6, paddingVertical: 2,
    letterSpacing: 0.3,
  },
  alertTime: { ...typography.paraXs, color: colors.textSoft },
});
