<template>
  <form @submit.prevent="submit" id="sign-up">
    <h1 class="font-semibold text-4xl mb-4">Sign up</h1>
    <p class="text-base mb-4 leading-5">
      Have an account?
      <router-link :to="{ name: 'login' }" class="font-semibold text-primary">Login</router-link>
    </p>
    <div class="form-row">
      <div class="form-group col-md-6">
        <label for="firstName">First Name</label>
        <input v-model="formData.first_name" type="text" class="form-control" id="firstName" required>
      </div>
      <div class="form-group col-md-6">
        <label for="lastName">Last Name</label>
        <input v-model="formData.last_name" type="text" class="form-control" id="lastName" required>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group col-md-6">
        <label for="userName">Username</label>
        <div class="input-group">
          <div class="input-group-prepend">
            <span class="input-group-text" id="validationTooltipUsernamePrepend">@</span>
          </div>
          <input v-model="formData.user_name" type="text" class="form-control" id="userName" placeholder="Username" required>
        </div>
      </div>
      <div class="form-group col-md-4">
        <label for="age">Your Age</label>
        <input v-model="formData.age" type="number" class="form-control" id="age" required>
      </div>
      <div class="form-group col-md-2">
        <label for="gender">Gender</label>
        <select v-model="formData.gender" id="gender" class="form-control" required>
          <option value="" disabled>Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>
      </div>
    </div>
    <div class="form-row">
      <div class="form-group col-md-6">
        <label for="phoneNumber">Phone Number</label>
        <input v-model="formData.phone_number" type="tel" class="form-control" id="phoneNumber" placeholder="Phone number" required>
      </div>
      <div class="form-group col-md-6">
        <label for="email">Email</label>
        <input v-model="formData.user_email" type="email" class="form-control" id="email" placeholder="Email" required>
      </div>
    </div>
    <div class="form-group">
      <label for="validationTooltip03" class="form-label">Password</label>
      <input v-model="formData.user_password" type="password" class="form-control" id="password" placeholder="Password" required>
      <ul class="password-rules">
        <li v-for="(rule, index) in passwordRules" :key="index">
          <span :class="{ 'text-success': rule(formData.user_password) === true, 'text-danger': rule(formData.user_password) !== true }">
            {{ rule(formData.user_password) !== true ? rule(formData.user_password) : '✔' }}
          </span>
        </li>
      </ul>
    </div>
    <div class="form-group">
      <label for="repeatPassword">Confirm Password</label>
      <input v-model="formData.repeatPassword" type="password" class="form-control" id="repeatPassword" placeholder="Password" required>
    </div>
    <button type="submit" id="signup-btn" class="w-full btn btn-primary">Sign Up</button>
  </form>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

const passwordRules = [
  (v) => !!v || 'Password field is required',
  (v) => (v && v.length >= 8) || 'Password must be at least 8 characters long',
  (v) => (v && /[A-Za-z]/.test(v)) || 'Password must contain at least one letter',
  (v) => (v && /\d/.test(v)) || 'Password must contain at least one number',
  (v) => (v && /[!@#$%^&*(),.?":{}|<>]/.test(v)) || 'Password must contain at least one special character',
];

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
        if (formData.gender === '') {
          alert('Please select your gender.');
          return;
        }

        if (formData.user_password !== formData.repeatPassword) {
          alert('Passwords do not match.');
          return;
        }

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

          router.push({ name: 'login' });
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
      passwordRules,
      submit,
    };
  },
};
</script>

<style scoped>
.password-rules {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.password-rules li {
  margin-bottom: 5px;
}

.text-success {
  color: green;
}

.text-danger {
  color: red;
}
</style>