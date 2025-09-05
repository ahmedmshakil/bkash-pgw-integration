<template>
  <div class="dashboard">
    <h1 class="page-title">Dashboard</h1>
    
    <div class="dashboard-grid">
      <div class="dashboard-card">
        <h3>Active Subscriptions</h3>
        <div v-if="!loading && subscriptions.length > 0">
          <div 
            v-for="subscription in subscriptions" 
            :key="subscription.id"
            class="subscription-item"
          >
            <div class="subscription-info">
              <h4>{{ getSubscriptionName(subscription.subscription_id) }}</h4>
              <span class="status" :class="subscription.status">
                {{ subscription.status }}
              </span>
            </div>
            <div class="subscription-date">
              Started: {{ formatDate(subscription.created_at) }}
            </div>
          </div>
        </div>
        <div v-else-if="!loading && subscriptions.length === 0" class="no-data">
          No active subscriptions
        </div>
        <div v-if="loading" class="loading">
          Loading subscriptions...
        </div>
      </div>
      
      <div class="dashboard-card">
        <h3>Quick Actions</h3>
        <div class="actions">
          <router-link to="/subscriptions" class="btn btn-primary">
            Browse Plans
          </router-link>
          <button @click="refreshData" class="btn btn-secondary">
            Refresh Data
          </button>
        </div>
      </div>
      
      <div class="dashboard-card">
        <h3>Account Info</h3>
        <div class="account-info">
          <p><strong>Total Subscriptions:</strong> {{ subscriptions.length }}</p>
          <p><strong>Account Status:</strong> Active</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'Dashboard',
  setup() {
    const subscriptions = ref([])
    const loading = ref(true)
    
    const subscriptionNames = {
      1: 'Basic Plan',
      2: 'Premium Plan', 
      3: 'Pro Plan'
    }
    
    const getSubscriptionName = (id) => {
      return subscriptionNames[id] || 'Unknown Plan'
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }
    
    const fetchSubscriptions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/user/subscriptions')
        subscriptions.value = response.data
      } catch (error) {
        console.error('Failed to fetch subscriptions:', error)
      } finally {
        loading.value = false
      }
    }
    
    const refreshData = () => {
      loading.value = true
      fetchSubscriptions()
    }
    
    onMounted(() => {
      fetchSubscriptions()
    })
    
    return {
      subscriptions,
      loading,
      getSubscriptionName,
      formatDate,
      refreshData
    }
  }
}
</script>

<style scoped>
.dashboard {
  color: white;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.dashboard-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.dashboard-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #ff6b6b;
}

.subscription-item {
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  margin-bottom: 1rem;
}

.subscription-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.subscription-info h4 {
  font-size: 1.1rem;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
}

.status.active {
  background: rgba(76, 175, 80, 0.3);
  color: #4caf50;
}

.status.expired {
  background: rgba(244, 67, 54, 0.3);
  color: #f44336;
}

.subscription-date {
  font-size: 0.9rem;
  opacity: 0.8;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.account-info p {
  margin-bottom: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.account-info p:last-child {
  border-bottom: none;
}

.no-data, .loading {
  text-align: center;
  opacity: 0.8;
  padding: 2rem;
}
</style>