<template>
	<br>
	<div>
    <!-- breadcrumb-section -->
    <div class="breadcrumb-section breadcrumb-bg">
      	<div class="container">
        <div class="row">
          <div class="col-lg-8 offset-lg-2 text-center">
            <div class="breadcrumb-text">
              <h1>Contact us</h1>
            </div>
          </div>
        </div>
      	</div>
    </div>
    <!-- end breadcrumb section -->

    <!-- contact form -->
    <div class="contact-from-section mt-150 mb-150">
      	<div class="container">
        <div class="row">
          	<div class="col-lg-8 mb-5 mb-lg-0">
            <div class="form-title">
              <h2>Have any questions?</h2>
              <p>We’re here to help! Whether you need more information about our services, have a query about your account, or just want to give us feedback, feel free to reach out. Our team is dedicated to providing you with the best possible support and will respond to your inquiries as soon as possible.</p>
            </div>
            <div id="form_status"></div>
            <div class="contact-form">
              <form @submit.prevent="submitForm" class="row g-3">
                <div class="col-md-6">
                  <label for="inputEmail4" class="form-label">Email</label>
                  <input type="email" class="form-control" v-model="form.email" required>
                </div>
                <div class="col-md-6">
                  <label for="name" class="form-label">Full Name</label>
                  <input type="text" class="form-control" v-model="form.full_name" required>
                </div>
                <div class="col-md-6">
                  <label for="subject" class="form-label">Subject</label>
                  <input type="text" class="form-control" v-model="form.subject" required>
                </div>
                <div class="col-md-6">
                  <label for="tel" class="form-label">Phone Number</label>
                  <input type="tel" class="form-control" v-model="form.phone_number" required>
                </div>
                <div class="form-floating">
                  <textarea class="form-control" placeholder="Leave a comment here" rows="10" v-model="form.message" style="height: 200px" required></textarea>
                </div>
                <div class="col-12">
                  <button type="submit" class="btn btn-primary">Submit</button>
                </div>
              </form>
            </div>
          	</div>
          	<div class="col-lg-4">
            <div class="contact-form-wrap">
              <div class="contact-form-box">
                <h4><i class="fas fa-map"></i> Our Address</h4>
                <p>34/8, East Karapul <br> Rabango <br> SA</p>
              </div>
              <div class="contact-form-box">
                <h4><i class="far fa-clock"></i> Active Hours</h4>
                <p>MON - FRIDAY: 8 to 9 PM <br> SAT - SUN: 10 to 8 PM </p>
              </div>
              <div class="contact-form-box">
                <h4><i class="fas fa-address-book"></i> Contact</h4>
                <p>Phone: +00 111 222 3333 <br> Email: support@empowerher.com</p>
              </div>
            </div>
          	</div>
        </div>
      	</div>
    </div>
    <!-- end contact form -->
	</div>
</template>

<script>
import api from '../api.js';
import qs from 'qs';

export default {
  data() {
    return {
      form: {
        email: '',
        full_name: '',
        subject: '',
        phone_number: '',
        message: ''
      }
    };
  },
  methods: {
    async submitForm() {
      const formData = qs.stringify(this.form);

      try {
        const response = await api.contactForm(formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        });
        alert('Your message has been sent successfully.', response.data);

        /** this clears the form after successful submission **/
        this.form.email = '';
        this.form.full_name = '';
        this.form.subject = '';
        this.form.phone_number = '';
        this.form.message = '';
      } catch (error) {
        console.error('There was an error sending the email:', error.response?.data || error.message);
        alert('There was an error sending your message. Please try again later.');
      }
    }
  }
};
</script>
