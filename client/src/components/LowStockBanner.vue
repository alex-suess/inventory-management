<template>
  <div v-if="count > 0" class="low-stock-banner" role="status">
    <span class="banner-text">{{ t('alerts.bannerText', { count }) }}</span>
    <router-link to="/inventory" class="banner-link">{{ t('alerts.bannerLink') }}</router-link>
  </div>
</template>

<script>
import { useI18n } from '../composables/useI18n'
import { useLowStockAlerts } from '../composables/useLowStockAlerts'

export default {
  name: 'LowStockBanner',
  setup() {
    const { t } = useI18n()
    const { count } = useLowStockAlerts()
    return { t, count }
  }
}
</script>

<style scoped>
.low-stock-banner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
  margin-bottom: var(--space-6);
  padding: var(--space-3) var(--space-4);
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-left: 4px solid var(--color-danger);
  border-radius: var(--radius-md);
  color: #991b1b;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
}

.banner-link {
  color: #991b1b;
  font-weight: var(--font-semibold);
  text-decoration: underline;
}

.banner-link:hover {
  color: var(--color-danger);
}
</style>
