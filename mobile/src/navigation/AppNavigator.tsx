import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

import { colors, radius, shadow } from '../constants/theme';
import DashboardScreen    from '../screens/DashboardScreen';
import AlertsScreen       from '../screens/AlertsScreen';
import SensorDetailScreen from '../screens/SensorDetailScreen';
import FarmsScreen        from '../screens/FarmsScreen';
import ProfileScreen      from '../screens/ProfileScreen';

const Tab   = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function TabIcon({ icon, label, focused }: { icon: string; label: string; focused: boolean }) {
  return (
    <View style={[styles.tabIcon, focused && styles.tabIconActive]}>
      <Text style={styles.tabEmoji}>{icon}</Text>
      {focused && <Text style={styles.tabLabel}>{label}</Text>}
    </View>
  );
}

function HomeStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Dashboard"    component={DashboardScreen} />
      <Stack.Screen name="SensorDetail" component={SensorDetailScreen} />
    </Stack.Navigator>
  );
}

function AlertsStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="AlertsList"   component={AlertsScreen} />
      <Stack.Screen name="SensorDetail" component={SensorDetailScreen} />
    </Stack.Navigator>
  );
}

function FarmsStack() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="FarmsList"    component={FarmsScreen} />
      <Stack.Screen name="SensorDetail" component={SensorDetailScreen} />
    </Stack.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{ headerShown: false }}
        tabBar={props => <CustomTabBar {...props} />}
      >
        <Tab.Screen name="Home"    component={HomeStack}    options={{ title: 'Bosh sahifa' }} />
        <Tab.Screen name="Farms"   component={FarmsStack}   options={{ title: 'Fermalar' }} />
        <Tab.Screen name="Alerts"  component={AlertsStack}  options={{ title: 'Alertlar' }} />
        <Tab.Screen name="Profile" component={ProfileScreen} options={{ title: 'Profil' }} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

function CustomTabBar({ state, descriptors, navigation }: any) {
  const TAB_ICONS = ['🏠', '🌾', '🔔', '👤'];

  return (
    <View style={styles.tabBar}>
      {state.routes.map((route: any, i: number) => {
        const focused  = state.index === i;
        const { options } = descriptors[route.key];

        return (
          <TabIcon
            key={route.key}
            icon={TAB_ICONS[i]}
            label={options.title ?? route.name}
            focused={focused}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    flexDirection: 'row',
    backgroundColor: '#111',
    paddingBottom: 20,
    paddingTop: 10,
    paddingHorizontal: 16,
    justifyContent: 'space-around',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    ...shadow.md,
  },
  tabIcon: {
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: radius.full,
    gap: 2,
  },
  tabIconActive: {
    backgroundColor: 'rgba(255,255,255,0.1)',
    flexDirection: 'row',
    gap: 6,
  },
  tabEmoji: { fontSize: 20 },
  tabLabel: { color: 'white', fontSize: 12, fontWeight: '600' },
});
