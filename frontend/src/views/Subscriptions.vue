<template>
  <div class="subscriptions">
    <h1 class="page-title">Choose Your Plan</h1>
    <p class="page-subtitle">Select a subscription plan that fits your needs</p>
    
    <div class="plans-grid" v-if="!loading">
      <div 
        v-for="plan in plans" 
        :key="plan.id" 
        class="plan-card"
        :class="{ 'popular': plan.id === 2 }"
      >
        <div class="plan-header">
          <h3 class="plan-name">{{ plan.name }}</h3>
          <div class="plan-price">
            <span class="currency">৳</span>
            <span class="amount">{{ plan.price }}</span>
            <span class="period">/{{ plan.duration }}</span>
          </div>
        </div>
        
        <div class="plan-features">
          <div class="feature" v-for="feature in getFeatures(plan.id)" :key="feature">
            ✓ {{ feature }}
          </div>
        </div>
        
        <button 
          @click="selectPlan(plan)" 
          class="btn btn-primary plan-btn"
        >
          Choose Plan
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      Loading plans...
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Subscriptions',
  setup() {
    const router = useRouter()
    const plans = ref([])
    const loading = ref(true)
    
    const getFeatures = (planId) => {
      const features = {
        1: ['Basic Support', '5 Projects', '10GB Storage'],
        2: ['Priority Support', '20 Projects', '50GB Storage', 'Advanced Analytics'],
        3: ['24/7 Support', 'Unlimited Projects', '200GB Storage', 'Advanced Analytics', 'Custom Integrations']
      }
      return features[planId] || []
    }
    
    const fetchPlans = async () => {
      try {
        const response = await axios.get('http://localhost:8000/subscriptions')
        plans.value = response.data
      } catch (error) {
        console.error('Failed to fetch plans:', error)
      } finally {
        loading.value = false
      }
    }
    
    const selectPlan = (plan) => {
      router.push(`/payment/${plan.id}`)
    }
    
    onMounted(() => {
      fetchPlans()
    })
    
    return {
      plans,
      loading,
      getFeatures,
      selectPlan
    }
  }
}
</script>

<style scoped>
.subscriptions {
  color: white;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.page-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.plan-card {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 2rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.plan-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.plan-card.popular {
  border: 2px solid #ff6b6b;
  transform: scale(1.05);
}

.plan-card.popular::before {
  content: 'Most Popular';
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: #ff6b6b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
}

.plan-header {
  margin-bottom: 2rem;
}

.plan-name {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.plan-price {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.2rem;
}

.currency {
  font-size: 1.2rem;
}

.amount {
  font-size: 2.5rem;
  font-weight: bold;
}

.period {
  font-size: 1rem;
  opacity: 0.8;
}

.plan-features {
  text-align: left;
  margin-bottom: 2rem;
}

.feature {
  padding: 0.5rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.feature:last-child {
  border-bottom: none;
}

.plan-btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.loading {
  font-size: 1.2rem;
  opacity: 0.8;
}
</style>