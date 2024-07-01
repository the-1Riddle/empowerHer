<template>
  <form @submit.prevent="submit">
    <h1 class="font-semibold text-4xl mb-4">Sign up</h1>
    <p class="text-base mb-4 leading-5">
      Have an account?
      <router-link :to="{ name: 'login' }" class="font-semibold text-primary">Login</router-link>
    </p>
    <div class="mb-4">
      <label for="userName" class="block mb-2">Username</label>
      <input
        v-model="formData.user_name"
        type="text"
        id="userName"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="firstName" class="block mb-2">First Name</label>
      <input
        v-model="formData.first_name"
        type="text"
        id="firstName"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="lastName" class="block mb-2">Last Name</label>
      <input
        v-model="formData.last_name"
        type="text"
        id="lastName"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="age" class="block mb-2">Age</label>
      <input
        v-model="formData.age"
        type="number"
        id="age"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="phoneNumber" class="block mb-2">Phone Number</label>
      <input
        v-model="formData.phone_number"
        type="tel"
        id="phoneNumber"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="email" class="block mb-2">Email</label>
      <input
        v-model="formData.user_email"
        type="email"
        id="email"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="password" class="block mb-2">Password</label>
      <input
        v-model="formData.user_password"
        type="password"
        id="password"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="repeatPassword" class="block mb-2">Repeat Password</label>
      <input
        v-model="formData.repeatPassword"
        type="password"
        id="repeatPassword"
        class="border p-2 w-full"
        required
      />
    </div>
    <div class="mb-4">
      <label for="gender" class="block mb-2">Gender</label>
      <select v-model="formData.gender" id="gender" class="border p-2 w-full" required>
        <option value="">Select Gender</option>
        <option value="male">Male</option>
        <option value="female">Female</option>
        <option value="other">Other</option>
      </select>
    </div>
    <div class="flex justify-center mt-4">
      <button class="w-full bg-blue-500 text-white p-2" type="submit">Create account</button>
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
      user_name: '',
      first_name: '',
      last_name: '',
      age: '',
      phone_number: '',
      user_email: '',
      user_password: '',
      repeatPassword: '',
      gender: '',
    });

    const submit = async () => {
      try {
        if (formData.gender.toLowerCase() === 'male') {
          alert('Signup not allowed for male gender.');
          return;
        }

        console.log('Form Data:', formData);

        const response = await api.createUser({
          user_name: formData.user_name,
          first_name: formData.first_name,
          last_name: formData.last_name,
          age: formData.age,
          phone_number: formData.phone_number,
          user_email: formData.user_email,
          user_password: formData.user_password,
        });

        console.log('Response:', response);

        if (response.status === 200 && response.data) {
          alert('You\'ve successfully signed up');
          router.push({ name: 'home' });
        } else {
          throw new Error('Signup failed');
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Signup failed. Please check your details and try again.');
      }
    };

    return {
      formData,
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
</style>
