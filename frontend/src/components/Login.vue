<template>
  <form @submit.prevent="submit">
    <h1 class="font-semibold text-4xl mb-4">Log in</h1>
    <p class="text-base mb-4 leading-5">
      New to our platform?
      <router-link :to="{ name: 'signup' }" class="font-semibold text-primary">Sign up</router-link>
    </p>
    <div class="mb-4">
      <label for="username" class="block mb-2">Username</label>
      <input
        v-model="formData.username"
        type="text"
        id="username"
        class="border p-2 w-full"
        required
      />
      <span v-if="errors.username" class="text-red-500">{{ errors.username }}</span>
    </div>
    <div class="mb-4">
      <label for="password" class="block mb-2">Password</label>
      <input
        v-model="formData.password"
        type="password"
        id="password"
        class="border p-2 w-full"
        required
      />
      <span v-if="errors.password" class="text-red-500">{{ errors.password }}</span>
    </div>
    <div class="flex justify-center mt-4">
      <button class="w-full bg-blue-500 text-white p-2" type="submit">Login</button>
    </div>
  </form>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

export default {
  setup() {
    const router = useRouter();
    
    const formData = reactive({
      username: '',
      password: '',
    });

    const errors = reactive({
      username: '',
      password: '',
    });

    const submit = async () => {
      try {
        const response = await api.loginUser(formData);
        if (response.data) {
          alert('You\'ve successfully logged in');
          router.push({ name: 'home' });
        }
      } catch (error) {
        console.error(error);
        alert('Login failed. Please check your credentials and try again.');
      }
    };

    return {
      formData,
      errors,
      submit,
    };
  },
};
</script>

<style>
.mb-4 {
  margin-bottom: 1rem;
}
.block {
  display: block;
}
.border {
  border: 1px solid #ccc;
}
.p-2 {
  padding: 0.5rem;
}
.w-full {
  width: 100%;
}
.bg-blue-500 {
  background-color: #3b82f6;
}
.text-white {
  color: white;
}
.text-red-500 {
  color: #f56565;
}
</style>
