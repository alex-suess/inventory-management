<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="close">
        <div
          class="modal-container"
          role="dialog"
          aria-modal="true"
          aria-labelledby="low-stock-title"
          @click.stop
        >
          <div class="modal-header">
            <h3 id="low-stock-title" class="modal-title">{{ t('alerts.title') }}</h3>
            <button class="close-button" type="button" :aria-label="t('alerts.closeAria')" @click="close">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <p class="panel-heading">{{ t('alerts.panelHeading') }}</p>

            <div v-if="loading && items.length === 0" class="state-text">{{ t('alerts.loading') }}</div>
            <div v-else-if="error" class="error">{{ error }}</div>
            <div v-else-if="items.length === 0" class="state-text">{{ t('alerts.empty') }}</div>

            <ul v-else class="alert-list">
              <li v-for="item in items" :key="item.id" class="alert-item">
                <div class="alert-main">
                  <span class="alert-name">{{ translateProductName(item.name) }}</span>
                  <span class="alert-meta">{{ item.sku }} · {{ translateWarehouse(item.location) }}</span>
                </div>
                <div class="alert-qty" :title="t('alerts.quantityLabel')">
                  <span class="badge danger">
                    {{ t('alerts.quantityOfReorder', { qty: item.quantity_on_hand, reorder: item.reorder_point }) }}
                  </span>
                </div>
              </li>
            </ul>
          </div>

          <div class="modal-footer">
            <router-link to="/inventory" class="inventory-link" @click="close">
              {{ t('alerts.viewInventory') }}
            </router-link>
            <button class="btn-secondary" type="button" @click="close">{{ t('common.close') }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
import { useI18n } from '../composables/useI18n'
import { useLowStockAlerts } from '../composables/useLowStockAlerts'

export default {
  name: 'LowStockAlertsModal',
  props: {
    isOpen: {
      type: Boolean,
      required: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const { t, translateProductName, translateWarehouse } = useI18n()
    const { items, loading, error } = useLowStockAlerts()

    const close = () => {
      emit('close')
    }

    return { t, items, loading, error, translateProductName, translateWarehouse, close }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 640px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  display: flex;
  border-radius: 6px;
}

.close-button:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.modal-body {
  padding: 1.25rem 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.panel-heading {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.state-text {
  text-align: center;
  padding: 2rem 0;
  color: #64748b;
}

.alert-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.alert-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-left: 4px solid var(--color-danger);
  border-radius: 8px;
}

.alert-main {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  min-width: 0;
}

.alert-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 0.875rem;
}

.alert-meta {
  color: #64748b;
  font-size: 0.75rem;
}

.alert-qty {
  flex-shrink: 0;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.inventory-link {
  color: var(--color-primary);
  font-weight: 600;
  font-size: 0.875rem;
}

.btn-secondary {
  padding: 0.5rem 1.25rem;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
