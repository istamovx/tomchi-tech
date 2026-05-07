import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import type { SensorReading, SensorConfig } from '../services/api';

const CROP_EMOJI: Record<string, string> = {
  pomidor:      '🍅',
  kartoshka:    '🥔',
  paxta:        '🌿',
  uzum:         '🍇',
  bugdoy:       '🌾',
  "makkajo'xori": '🌽',
  piyoz:        '🧅',
};

interface Props {
  reading: SensorReading;
  config?: SensorConfig;
  onPress?: () => void;
}

function getMoistureStatus(moisture: number, threshold: number) {
  if (moisture < threshold - 15) return { label: 'Darhol sug\'or!', color: colors.danger,   bg: colors.dangerBg  };
  if (moisture < threshold)      return { label: 'Tez sug\'or',     color: colors.warning,  bg: colors.warningBg };
  if (moisture > 80)             return { label: 'Yuqori',          color: colors.neutral,  bg: colors.neutralBg };
  return                                { label: 'Yaxshi',          color: colors.success,  bg: colors.successBg };
}

function getStatusDotColor(status: string) {
  if (status === 'online')  return colors.success;
  if (status === 'warning') return colors.warning;
  return colors.neutral;
}

export default function SensorCard({ reading, config, onPress }: Props) {
  const threshold = config?.irrigation_threshold ?? 45;
  const status    = getMoistureStatus(reading.soil_moisture, threshold);
  const offline   = config?.status === 'offline';
  const emoji     = CROP_EMOJI[config?.crop_type ?? ''] ?? '🌱';

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      {/* Left accent bar */}
      <View style={[styles.accent, { backgroundColor: status.color }]} />

      <View style={styles.content}>
        {/* Top row */}
        <View style={styles.topRow}>
          <Text style={styles.emoji}>{emoji}</Text>
          <View style={styles.idWrap}>
            <Text style={styles.sensorId}>{reading.sensor_id}</Text>
            <Text style={styles.cropName}>{config?.crop_type ?? '—'}</Text>
          </View>
          <View style={[styles.badge, { backgroundColor: status.bg }]}>
            <Text style={[styles.badgeText, { color: status.color }]}>{status.label}</Text>
          </View>
        </View>

        {/* Moisture bar */}
        <View style={styles.barWrap}>
          <View style={styles.barTrack}>
            <View style={[
              styles.barFill,
              {
                width: `${offline ? 0 : reading.soil_moisture}%`,
                backgroundColor: status.color,
              },
            ]} />
          </View>
          <Text style={[styles.pct, { color: offline ? colors.neutral : status.color }]}>
            {offline ? '—' : `${reading.soil_moisture.toFixed(1)}%`}
          </Text>
        </View>

        {/* Stats row */}
        <View style={styles.statsRow}>
          <View style={styles.stat}>
            <Text style={styles.statIcon}>🌡</Text>
            <Text style={styles.statVal}>
              {offline ? '—' : `${reading.temperature.toFixed(1)}°C`}
            </Text>
          </View>
          <View style={styles.stat}>
            <Text style={styles.statIcon}>💧</Text>
            <Text style={styles.statVal}>
              {offline ? '—' : `${reading.humidity.toFixed(0)}%`}
            </Text>
          </View>
          <View style={styles.stat}>
            <Text style={styles.statIcon}>🔋</Text>
            <Text style={[
              styles.statVal,
              reading.battery_level < 20 && !offline ? { color: colors.danger } : {},
            ]}>
              {offline ? '—' : `${reading.battery_level.toFixed(0)}%`}
            </Text>
          </View>
          <View style={styles.stat}>
            <View style={[styles.statusDot, {
              backgroundColor: getStatusDotColor(config?.status ?? 'offline'),
            }]} />
            <Text style={styles.statVal}>{config?.status ?? 'offline'}</Text>
          </View>
        </View>

        {/* Location */}
        {config && (
          <Text style={styles.location}>
            📍 {config.field_area_ha} ga
            {config.farm_id ? ` · ${config.farm_id}` : ''}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  card: {
    flexDirection: 'row',
    backgroundColor: colors.bgWhite,
    borderRadius: radius.lg,
    marginBottom: spacing.sm,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: colors.stroke,
    ...shadow.sm,
  },
  accent: {
    width: 4,
  },
  content: {
    flex: 1,
    padding: spacing.md,
    gap: 8,
  },
  topRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  emoji: {
    fontSize: 24,
  },
  idWrap: { flex: 1 },
  sensorId: {
    ...typography.labelSm,
    color: colors.textStrong,
  },
  cropName: {
    ...typography.paraXs,
    color: colors.textSoft,
    marginTop: 1,
  },
  badge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: radius.full,
  },
  badgeText: {
    fontSize: 11,
    fontWeight: '600',
  },
  barWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginTop: 2,
  },
  barTrack: {
    flex: 1,
    height: 6,
    backgroundColor: colors.bgSoft,
    borderRadius: radius.full,
    overflow: 'hidden',
  },
  barFill: {
    height: '100%',
    borderRadius: radius.full,
  },
  pct: {
    ...typography.labelSm,
    width: 44,
    textAlign: 'right',
  },
  statsRow: {
    flexDirection: 'row',
    gap: spacing.md,
    marginTop: 2,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
  },
  statIcon: { fontSize: 12 },
  statVal: {
    ...typography.paraXs,
    color: colors.textSub,
  },
  statusDot: {
    width: 7,
    height: 7,
    borderRadius: radius.full,
  },
  location: {
    ...typography.paraXs,
    color: colors.textSoft,
    marginTop: 2,
  },
});
