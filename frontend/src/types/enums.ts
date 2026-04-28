export const EPSG = {
  STANDARD: 4326,
} as const;

export type EPSG = (typeof EPSG)[keyof typeof EPSG];
