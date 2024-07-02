<!-- src/views/Login.vue -->
<template>
  <!-- Your login form -->
</template>

<script>
import { mapActions } from 'vuex';

export default {
  methods: {
    ...mapActions(['login']),
    async handleLogin() {
      // Perform login logic here

      // On successful login:
      this.login();
      this.$router.push({ name: 'home' });
    },
  },
};
</script>

vue

<!-- src/views/Signup.vue -->
<template>
  <!-- Your signup form -->
</template>

<script>
import { mapActions } from 'vuex';

export default {
  methods: {
    ...mapActions(['login']),
    async handleSignup() {
      // Perform signup logic here

      // On successful signup:
      this.login();
      this.$router.push({ name: 'home' });
    },
  },
};
</script>