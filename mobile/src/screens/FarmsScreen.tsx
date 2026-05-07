import React, { useEffect, useState, useCallback } from 'react';
import {
  View, Text, ScrollView, StyleSheet,
  RefreshControl, ActivityIndicator, TouchableOpacity, TextInput,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors, radius, spacing, typography, shadow } from '../constants/theme';
import { farmsApi, sensorsApi } from '../services/api';
import type { Farm, SensorConfig } from '../services/api';

const CROP_EMOJI: Record<string, string> = {
  pomidor:       '🍅',
  kartoshka:     '🥔',
  paxta:         '🌸',
  uzum:          '🍇',
  bugdoy:        '🌾',
  "makkajo'xori":'🌽',
  piyoz:         '🧅',
};

const CROP_LABEL: Record<string, string> = {
  pomidor:       'Pomidor',
  kartoshka:     'Kartoshka',
  paxta:         'Paxta',
  uzum:          'Uzum',
  bugdoy:        "Bug'doy",
  "makkajo'xori":"Makkajo'xori",
  piyoz:         'Piyoz',
};

function StatusDot({ online }: { online: number; total: number }) {
  const allGood = online > 0;
  return (
    <View style={[styles.dot, { backgroundColor: allGood ? colors.success : colors.danger }]} />
  );
}

export default function FarmsScreen({ navigation }: any) {
  const [farms, setFarms]       = useState<Farm[]>([]);
  const [configs, setConfigs]   = useState<SensorConfig[]>([]);
  const [loading, setLoading]   = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch]     = useState('');
  const [cropFilter, setCropFilter] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      const [f, c] = await Promise.all([farmsApi.getAll(), sensorsApi.getConfigs()]);
      setFarms(f);
      setConfigs(c);
    } catch { /* silent */ }
    finally { setLoading(false); setRefreshing(false); }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const onRefresh = () => { setRefreshing(true); fetchData(); };

  const onlineForFarm = (farmId: string) =>
    configs.filter(c => c.farm_id === farmId && c.status === 'online').length;

  const sensorsForFarm = (farmId: string) =>
    configs.filter(c => c.farm_id === farmId).length;

  const crops = [...new Set(farms.map(f => f.crop_type))];

  const filtered = farms.filter(f => {
    const matchSearch =
      !search ||
      f.farmer_name.toLowerCase().includes(search.toLowerCase()) ||
      f.farm_id.toLowerCase().includes(search.toLowerCase()) ||
      f.region.toLowerCase().includes(search.toLowerCase());
    const matchCrop = !cropFilter || f.crop_type === cropFilter;
    return matchSearch && matchCrop;
  });

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingTxt}>Fermalar yuklanmoqda...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>🌾 Fermalar</Text>
          <Text style={styles.subtitle}>{farms.length} ta ferma</Text>
        </View>
        <View style={styles.totalBadge}>
          <Text style={styles.totalTxt}>{farms.length}</Text>
        </View>
      </View>

      {/* Search */}
      <View style={styles.searchWrap}>
        <Text style={styles.searchIcon}>🔍</Text>
        <TextInput
          style={styles.searchInput}
          placeholder="Fermer ismi yoki hudud..."
          placeholderTextColor={colors.textSoft}
          value={search}
          onChangeText={setSearch}
          returnKeyType="search"
        />
        {!!search && (
          <TouchableOpacity onPress={() => setSearch('')}>
            <Text style={styles.clearBtn}>✕</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Crop filter chips */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.chips}
      >
        <TouchableOpacity
          style={[styles.chip, !cropFilter && styles.chipActive]}
          onPress={() => setCropFilter(null)}
        >
          <Text style={[styles.chipTxt, !cropFilter && styles.chipTxtActive]}>Barchasi</Text>
        </TouchableOpacity>
        {crops.map(crop => (
          <TouchableOpacity
            key={crop}
            style={[styles.chip, cropFilter === crop && styles.chipActive]}
            onPress={() => setCropFilter(cropFilter === crop ? null : crop)}
          >
            <Text style={styles.chipEmoji}>{CROP_EMOJI[crop] ?? '🌱'}</Text>
            <Text style={[styles.chipTxt, cropFilter === crop && styles.chipTxtActive]}>
              {CROP_LABEL[crop] ?? crop}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Farm list */}
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.list}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
        showsVerticalScrollIndicator={false}
      >
        {filtered.length === 0 ? (
          <View style={styles.empty}>
            <Text style={styles.emptyIcon}>🌾</Text>
            <Text style={styles.emptyTitle}>Fermalar topilmadi</Text>
            <Text style={styles.emptyTxt}>Qidiruvni o'zgartiring</Text>
          </View>
        ) : (
          filtered.map(farm => {
            const online  = onlineForFarm(farm.farm_id);
            const total   = sensorsForFarm(farm.farm_id) || farm.sensor_count;
            const allGood = online === total && total > 0;

            return (
              <TouchableOpacity
                key={farm.farm_id}
                style={styles.card}
                activeOpacity={0.75}
                onPress={() => navigation.navigate('SensorDetail', { farmId: farm.farm_id })}
              >
                {/* Card top */}
                <View style={styles.cardTop}>
                  <View style={styles.cropBadge}>
                    <Text style={styles.cropEmoji}>{CROP_EMOJI[farm.crop_type] ?? '🌱'}</Text>
                  </View>
                  <View style={styles.cardInfo}>
                    <View style={styles.cardTitleRow}>
                      <Text style={styles.farmerName} numberOfLines={1}>{farm.farmer_name}</Text>
                      <View style={[styles.statusBadge, { backgroundColor: allGood ? colors.successBg : colors.dangerBg }]}>
                        <StatusDot online={online} total={total} />
                        <Text style={[styles.statusTxt, { color: allGood ? colors.success : colors.danger }]}>
                          {allGood ? 'Yaxshi' : 'Muammo'}
                        </Text>
                      </View>
                    </View>
                    <Text style={styles.farmId}>{farm.farm_id}</Text>
                  </View>
                </View>

                {/* Divider */}
                <View style={styles.divider} />

                {/* Stats row */}
                <View style={styles.statsRow}>
                  <View style={styles.stat}>
                    <Text style={styles.statLabel}>Hudud</Text>
                    <Text style={styles.statValue}>{farm.region}</Text>
                  </View>
                  <View style={styles.statDivider} />
                  <View style={styles.stat}>
                    <Text style={styles.statLabel}>Maydon</Text>
                    <Text style={styles.statValue}>{farm.total_area_ha} ga</Text>
                  </View>
                  <View style={styles.statDivider} />
                  <View style={styles.stat}>
                    <Text style={styles.statLabel}>Sensorlar</Text>
                    <Text style={styles.statValue}>
                      <Text style={{ color: colors.success }}>{online}</Text>/{total}
                    </Text>
                  </View>
                  <View style={styles.statDivider} />
                  <View style={styles.stat}>
                    <Text style={styles.statLabel}>Ekin</Text>
                    <Text style={styles.statValue}>{CROP_LABEL[farm.crop_type] ?? farm.crop_type}</Text>
                  </View>
                </View>

                {/* Phone */}
                <View style={styles.phoneRow}>
                  <Text style={styles.phoneIcon}>📞</Text>
                  <Text style={styles.phoneTxt}>{farm.phone}</Text>
                  <Text style={styles.districtTxt}>{farm.district} tumani</Text>
                </View>
              </TouchableOpacity>
            );
          })
        )}
        <View style={{ height: 24 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe:       { flex: 1, backgroundColor: colors.bgWeak },
  center:     { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: colors.bgWeak, gap: spacing.sm },
  loadingTxt: { ...typography.paraSm, color: colors.textSub },

  header:     { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.lg, paddingTop: spacing.md, paddingBottom: spacing.sm },
  title:      { ...typography.h2, color: colors.textStrong },
  subtitle:   { ...typography.paraSm, color: colors.textSub, marginTop: 2 },
  totalBadge: { backgroundColor: colors.primaryLight, borderRadius: radius.full, minWidth: 32, height: 32, justifyContent: 'center', alignItems: 'center', paddingHorizontal: spacing.sm },
  totalTxt:   { ...typography.labelMd, color: colors.primary },

  searchWrap: { flexDirection: 'row', alignItems: 'center', marginHorizontal: spacing.lg, marginBottom: spacing.sm, backgroundColor: colors.bgWhite, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.stroke, paddingHorizontal: spacing.md, ...shadow.xs },
  searchIcon: { fontSize: 16, marginRight: spacing.xs },
  searchInput:{ flex: 1, ...typography.paraSm, color: colors.textStrong, paddingVertical: spacing.sm },
  clearBtn:   { fontSize: 14, color: colors.textSoft, padding: 4 },

  chips:      { paddingHorizontal: spacing.lg, paddingBottom: spacing.sm, gap: spacing.xs, flexDirection: 'row' },
  chip:       { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.md, paddingVertical: 6, borderRadius: radius.full, backgroundColor: colors.bgWhite, borderWidth: 1, borderColor: colors.stroke, gap: 4 },
  chipActive: { backgroundColor: colors.primaryLight, borderColor: colors.primary },
  chipEmoji:  { fontSize: 13 },
  chipTxt:    { ...typography.labelSm, color: colors.textSub },
  chipTxtActive:{ color: colors.primary },

  scroll:     { flex: 1 },
  list:       { padding: spacing.lg, gap: spacing.md },

  card:       { backgroundColor: colors.bgWhite, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.stroke, overflow: 'hidden', ...shadow.sm },
  cardTop:    { flexDirection: 'row', alignItems: 'center', padding: spacing.lg, gap: spacing.md },
  cropBadge:  { width: 48, height: 48, borderRadius: radius.md, backgroundColor: colors.bgSoft, justifyContent: 'center', alignItems: 'center' },
  cropEmoji:  { fontSize: 24 },
  cardInfo:   { flex: 1 },
  cardTitleRow: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', gap: spacing.sm },
  farmerName: { ...typography.labelLg, color: colors.textStrong, flex: 1 },
  farmId:     { ...typography.paraXs, color: colors.textSoft, marginTop: 2 },

  statusBadge:{ flexDirection: 'row', alignItems: 'center', gap: 4, paddingHorizontal: 8, paddingVertical: 3, borderRadius: radius.full },
  dot:        { width: 6, height: 6, borderRadius: 3 },
  statusTxt:  { ...typography.paraXs, fontWeight: '600' },

  divider:    { height: 1, backgroundColor: colors.stroke, marginHorizontal: spacing.lg },

  statsRow:   { flexDirection: 'row', paddingVertical: spacing.md },
  stat:       { flex: 1, alignItems: 'center', paddingVertical: 4 },
  statLabel:  { ...typography.paraXs, color: colors.textSoft, marginBottom: 2 },
  statValue:  { ...typography.labelSm, color: colors.textStrong },
  statDivider:{ width: 1, backgroundColor: colors.stroke, marginVertical: 4 },

  phoneRow:   { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, paddingBottom: spacing.md, gap: spacing.xs },
  phoneIcon:  { fontSize: 13 },
  phoneTxt:   { ...typography.paraSm, color: colors.textSub, flex: 1 },
  districtTxt:{ ...typography.paraXs, color: colors.textSoft },

  empty:      { alignItems: 'center', paddingTop: 80, gap: spacing.sm },
  emptyIcon:  { fontSize: 48 },
  emptyTitle: { ...typography.h3, color: colors.textStrong },
  emptyTxt:   { ...typography.paraSm, color: colors.textSub },
});
