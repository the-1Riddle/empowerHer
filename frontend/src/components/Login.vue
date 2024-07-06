<template>
  <form @submit.prevent="submit" id="sign-up">
    <h1 class="font-semibold text-4xl mb-4">Log in</h1>
    <p class="text-base mb-4 leading-5">
      New to our platform?
      <router-link :to="{ name: 'signup' }" class="font-semibold text-primary">Sign up</router-link>
    </p>
    <div class="mb-4">
      <label for="username" class="block mb-2">User Email</label>
      <input
        v-model="formData.username"
        type="email"
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
      <button class="w-full btn-primary text-white p-2" type="submit">Login</button>
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
        console.log("Submitting login data:", formData);
        const response = await api.loginUser({
          username: formData.username,
          password: formData.password,
        });
        console.log("Login response:", response);
        if (response.data) {
          alert('You\'ve successfully logged in');
          localStorage.setItem('user-info', response.data.access_token);
          router.push({ name: 'home' });
        }
      } catch (error) {
        console.error("Login error:", error);
        alert('Login failed. Please check your credentials and try again.');
      }
    };

    return {
      formData,
      errors,
      submit,
    };
  },
  mounted() {
    let user = localStorage.getItem('user-info');
    if (user) {
      this.$router.push({ name: 'home' });
    }
  },
};
</script>

<style>

</style>
