<template>
  <div class="payment">
    <div class="payment-container">
      <div class="payment-card">
        <h2>Complete Your Payment</h2>
        
        <div v-if="selectedPlan" class="plan-summary">
          <h3>{{ selectedPlan.name }}</h3>
          <div class="price">৳{{ selectedPlan.price }}/{{ selectedPlan.duration }}</div>
        </div>
        
        <div class="payment-method">
          <h4>Payment Method</h4>
          <div class="bkash-info">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiB2aWV3Qm94PSIwIDAgMTAwIDQwIiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cmVjdCB3aWR0aD0iMTAwIiBoZWlnaHQ9IjQwIiByeD0iOCIgZmlsbD0iI0UyMTM2RiIvPgo8dGV4dCB4PSI1MCIgeT0iMjUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZm9udC13ZWlnaHQ9ImJvbGQiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5ia2FzaDwvdGV4dD4KPHN2Zz4K" alt="bKash" class="bkash-logo" />
            <p>Pay securely with bKash</p>
          </div>
        </div>
        
        <button 
          @click="initiatePayment" 
          class="btn btn-primary payment-btn"
          :disabled="loading"
        >
          {{ loading ? 'Processing...' : `Pay ৳${selectedPlan?.price} with bKash` }}
        </button>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div v-if="paymentStatus" class="payment-status">
          <div v-if="paymentStatus === 'pending'" class="status-pending">
            <p>Payment initiated. Please complete the payment in the bKash app.</p>
            <button @click="checkPaymentStatus" class="btn btn-secondary">
              Check Payment Status
            </button>
          </div>
          
          <div v-if="paymentStatus === 'completed'" class="status-success">
            <p>✅ Payment completed successfully!</p>
            <router-link to="/dashboard" class="btn btn-primary">
              Go to Dashboard
            </router-link>
          </div>
          
          <div v-if="paymentStatus === 'failed'" class="status-failed">
            <p>❌ Payment failed. Please try again.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'Payment',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const selectedPlan = ref(null)
    const loading = ref(false)
    const error = ref('')
    const paymentStatus = ref('')
    const currentPaymentId = ref('')
    
    const plans = [
      { id: 1, name: "Basic Plan", price: 500, duration: "monthly" },
      { id: 2, name: "Premium Plan", price: 1000, duration: "monthly" },
      { id: 3, name: "Pro Plan", price: 2000, duration: "monthly" }
    ]
    
    const initiatePayment = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await axios.post('http://localhost:8000/payment/create', {
          subscription_id: selectedPlan.value.id,
          amount: selectedPlan.value.price
        })
        
        currentPaymentId.value = response.data.payment_id_bkash
        paymentStatus.value = 'pending'
        
        // In a real app, you would redirect to bKash URL
        // window.open(response.data.bkash_url, '_blank')
        
        // For demo purposes, simulate payment completion after 3 seconds
        setTimeout(() => {
          executePayment()
        }, 3000)
        
      } catch (err) {
        error.value = err.response?.data?.detail || 'Payment initiation failed'
      } finally {
        loading.value = false
      }
    }
    
    const executePayment = async () => {
      try {
        const response = await axios.post('http://localhost:8000/payment/execute', {
          payment_id: currentPaymentId.value
        })
        
        if (response.data.status === 'completed') {
          paymentStatus.value = 'completed'
        } else {
          paymentStatus.value = 'failed'
        }
      } catch (err) {
        paymentStatus.value = 'failed'
        error.value = 'Payment execution failed'
      }
    }
    
    const checkPaymentStatus = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/payment/status/${currentPaymentId.value}`)
        
        if (response.data.statusCode === '0000') {
          paymentStatus.value = 'completed'
        } else {
          paymentStatus.value = 'failed'
        }
      } catch (err) {
        error.value = 'Failed to check payment status'
      }
    }
    
    onMounted(() => {
      const planId = parseInt(route.params.planId)
      selectedPlan.value = plans.find(plan => plan.id === planId)
      
      if (!selectedPlan.value) {
        router.push('/subscriptions')
      }
    })
    
    return {
      selectedPlan,
      loading,
      error,
      paymentStatus,
      initiatePayment,
      checkPaymentStatus
    }
  }
}
</script>

<style scoped>
.payment {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.payment-container {
  width: 100%;
  max-width: 500px;
}

.payment-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  text-align: center;
}

.payment-card h2 {
  margin-bottom: 2rem;
  font-size: 2rem;
}

.plan-summary {
  background: rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.plan-summary h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.price {
  font-size: 2rem;
  font-weight: bold;
  color: #ff6b6b;
}

.payment-method {
  margin-bottom: 2rem;
}

.payment-method h4 {
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.bkash-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(226, 19, 111, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(226, 19, 111, 0.3);
}

.bkash-logo {
  height: 30px;
}

.payment-btn {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 1rem;
}

.btn-primary {
  background: linear-gradient(45deg, #E2136F, #C70E5C);
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  text-decoration: none;
  display: inline-block;
  margin-top: 1rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #ff6b6b;
  margin-top: 1rem;
  padding: 1rem;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 6px;
}

.payment-status {
  margin-top: 2rem;
  padding: 1.5rem;
  border-radius: 8px;
}

.status-pending {
  background: rgba(255, 193, 7, 0.2);
  border: 1px solid rgba(255, 193, 7, 0.3);
}

.status-success {
  background: rgba(76, 175, 80, 0.2);
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-failed {
  background: rgba(244, 67, 54, 0.2);
  border: 1px solid rgba(244, 67, 54, 0.3);
}
</style>