<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <a class="navbar-brand display-1" href="/"><h1>EmpowerHer</h1></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav">
        
      </ul>
      <ul class="nav ml-auto">
        <li class="nav-item active">
          <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="posts" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Posts
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="/posts">Posts</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="/wellness">Wellness</a>
            <a class="dropdown-item" href="/sexual-awareness">Sexual Awareness</a>
            <a class="dropdown-item" href="/gender-violence">Gender Violence</a>
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/about">About </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/contact">Contact </a>
        </li>
      </ul>
      <ul class="navbar-nav ml-auto">
        <li class="nav-item" v-if="!user">
          <a class="nav-link" href="/login"> Login</a>
        </li>
        <li class="nav-item" v-if="user">
          <a class="nav-link" href="javascript:void(0);" @click.prevent="openPopup">
            <span class="material-symbols-outlined">edit_square</span>
          </a>
          <CreatePost ref="popupForm" />
        </li>
        <li class="nav-item" v-if="user">
          <a class="nav-link" href="/account"> Account</a>
        </li>
        <li class="nav-item" v-if="user">
          <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
        </li>
      </ul>
    </div>
  </nav>
  <!-- end header -->
  <router-view />
</template>


<script>
import api from './api';
import CreatePost from './components/CreatePost.vue';

export default {
  name: 'Home',
  components: {
    CreatePost,
  },
  data() {
    return {
      user: null,
    };
  },
  mounted() {
    this.checkTokenAndFetchUser();
  },
  methods: {
    logout() {
      localStorage.removeItem('user-info');
      this.user = null;
      this.$router.push({ name: 'login' });
    },
    openPopup() {
      this.$refs.popupForm.open();
    },
    async checkTokenAndFetchUser() {
      let userInfo = localStorage.getItem('user-info');
      if (userInfo) {
        try {
          await api.getUserDetails();
          this.user = userInfo;
        } catch (error) {
          if (error.response && error.response.status === 401) {
            // logout the user if unauthorised
            this.logout();
          }
        }
      } else {
        this.$router.push({ name: 'login' });
      }
    }
  }
};
</script>

<style lang="scss">

</style>
