<template>
  <div v-if="show" class="popup">
    <div class="popup-content">
      <span class="close" @click="close">&times;</span>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="email" class="form-label">Email address</label>
          <input type="email" v-model="email" class="form-control" id="email" placeholder="name@example.com" required>
        </div>
        <div class="mb-3">
          <label for="title" class="form-label">Post Title</label>
          <input type="text" v-model="title" class="form-control" id="title" placeholder="This is a Post Title" required>
        </div>
        <div class="mb-3">
          <label for="message" class="form-label">Post Body</label>
          <textarea class="form-control" id="message" rows="3" v-model="message" required></textarea>
        </div>
        <div class="input-group mb-3">
          <input type="file" @change="handleFileUpload" class="form-control" id="inputGroupFile02">
          <label class="input-group-text" for="inputGroupFile02">Upload</label>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../api.js';

export default {
  setup() {
    const currentUser = ref('');

    const fetchUserDetails = async () => {
      try {
        const response = await api.getUserDetails();
        currentUser.value = response.data.user_email;
      } catch (error) {
        console.error("Failed to fetch user details:", error);
      }
    };

    onMounted(() => {
      fetchUserDetails();
    });

    return {
      currentUser
    };
  },
  data() {
    return {
      show: false,
      email: '', // will be set after fetching user details
      title: '',
      message: '',
      image: null,
    };
  },
  watch: {
    currentUser(newEmail) {
      this.email = newEmail;
    }
  },
  methods: {
    open() {
      this.show = true;
    },
    close() {
      this.show = false;
    },
    handleFileUpload(event) {
      this.image = event.target.files[0];
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('user_email', this.email);
      formData.append('post_title', this.title);
      formData.append('post_desc', this.message);
      if (this.image) {
        formData.append('image', this.image);
      }

      try {
        const response = await api.createPost(formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Form Submitted', response.data);
      } catch (error) {
        console.error('Form Submission Error', error.response?.data || error.message);
      }

      this.close();
    },
  },
};
</script>

<style>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure this is higher than other elements */
}

.popup-content {
  background: #fff;
  padding: 20px;
  border-radius: 5px;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
</style>
