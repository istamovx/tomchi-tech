// Tomchi Tech — Design Tokens (AlignUI asosida)
export const colors = {
  // Backgrounds
  bgWhite:    '#ffffff',
  bgWeak:     '#f7f7f7',
  bgSoft:     '#f0f0f0',

  // Text
  textStrong: '#171717',
  textSub:    '#5c5c5c',
  textSoft:   '#a3a3a3',

  // Borders
  stroke:     '#ebebeb',

  // Primary — Tomchi Tech yashil
  primary:    '#16a34a',
  primaryLight:'#dcfce7',

  // Status
  success:    '#22c55e',
  successBg:  '#f0fdf4',
  warning:    '#eab308',
  warningBg:  '#fef9c3',
  danger:     '#ef4444',
  dangerBg:   '#fee2e2',
  neutral:    '#94a3b8',
  neutralBg:  '#f1f5f9',
};

export const radius = {
  sm:   4,
  md:   8,
  lg:   10,
  full: 999,
};

export const spacing = {
  xs:  4,
  sm:  8,
  md:  12,
  lg:  16,
  xl:  20,
  xxl: 24,
};

export const typography = {
  // Label
  labelSm:  { fontSize: 14, fontWeight: '500' as const, lineHeight: 20, letterSpacing: -0.084 },
  labelMd:  { fontSize: 16, fontWeight: '500' as const, lineHeight: 22, letterSpacing: -0.16 },
  labelLg:  { fontSize: 18, fontWeight: '500' as const, lineHeight: 24, letterSpacing: -0.27 },

  // Paragraph
  paraXs:   { fontSize: 12, fontWeight: '400' as const, lineHeight: 16 },
  paraSm:   { fontSize: 14, fontWeight: '400' as const, lineHeight: 20, letterSpacing: -0.084 },

  // Heading
  h1:       { fontSize: 24, fontWeight: '700' as const, lineHeight: 32, letterSpacing: -0.48 },
  h2:       { fontSize: 20, fontWeight: '700' as const, lineHeight: 28, letterSpacing: -0.3 },
  h3:       { fontSize: 18, fontWeight: '600' as const, lineHeight: 24 },
};

export const shadow = {
  xs: {
    shadowColor: '#0A0D14',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.03,
    shadowRadius: 2,
    elevation: 1,
  },
  sm: {
    shadowColor: '#1B1C1D',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.08,
    shadowRadius: 12,
    elevation: 4,
  },
};
