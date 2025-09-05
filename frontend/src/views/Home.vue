<template>
  <div class="home">
    <div class="hero">
      <h1 class="hero-title">Welcome to Our Subscription Service</h1>
      <p class="hero-subtitle">Choose from our premium plans and pay securely with bKash</p>
      
      <div class="hero-actions">
        <router-link to="/subscriptions" class="btn btn-primary" v-if="isAuthenticated">
          View Plans
        </router-link>
        <router-link to="/register" class="btn btn-primary" v-else>
          Get Started
        </router-link>
        <router-link to="/login" class="btn btn-secondary" v-if="!isAuthenticated">
          Login
        </router-link>
      </div>
    </div>
    
    <div class="features">
      <div class="feature-card">
        <h3>Secure Payments</h3>
        <p>Pay safely with bKash integration</p>
      </div>
      <div class="feature-card">
        <h3>Flexible Plans</h3>
        <p>Choose the plan that fits your needs</p>
      </div>
      <div class="feature-card">
        <h3>Instant Access</h3>
        <p>Get immediate access after payment</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    return {
      isAuthenticated
    }
  }
}
</script>

<style scoped>
.home {
  text-align: center;
  color: white;
}

.hero {
  padding: 4rem 0;
}

.hero-title {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: bold;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: transform 0.3s, box-shadow 0.3s;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.btn-primary {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.feature-card p {
  opacity: 0.9;
}
</style>