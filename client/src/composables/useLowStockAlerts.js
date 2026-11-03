import { ref, computed, watch } from 'vue'
import { api } from '../api'
import { useFilters } from './useFilters'
import { useI18n } from './useI18n'

// Shared low-stock alert state (singleton pattern, like useFilters)
const items = ref([])
const loading = ref(false)
const error = ref(null)

let initialized = false
// Guards against out-of-order responses when filters change quickly
let requestId = 0

export function useLowStockAlerts() {
  const { selectedLocation, selectedCategory, getCurrentFilters } = useFilters()
  const { t } = useI18n()

  const count = computed(() => items.value.length)

  const refresh = async () => {
    const id = ++requestId
    loading.value = true
    error.value = null
    try {
      // Inventory has no time dimension: api only sends warehouse and category
      const result = await api.getLowStockItems(getCurrentFilters())
      if (id !== requestId) return
      items.value = result
    } catch (err) {
      if (id !== requestId) return
      items.value = []
      // Translated at error time, so it stays in the locale active when it failed
      error.value = t('alerts.loadError', { message: err.message })
    } finally {
      if (id === requestId) loading.value = false
    }
  }

  // Register the watcher once for the whole app, not once per consumer
  if (!initialized) {
    initialized = true
    watch([selectedLocation, selectedCategory], refresh)
  }

  return { items, count, loading, error, refresh }
}
