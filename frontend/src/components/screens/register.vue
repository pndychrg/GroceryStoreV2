<template>
    <div class="auth-wrapper my-4 container" style="min-height: 85vh;">
        <div class="auth-inner card">
            <form @submit.prevent="submitHandler">
                <h3>Register</h3>
                <br>
                <div class="form-group">
                    <label for="name">Name</label>
                    <input type="text" class="form-control" placeholder="Name" v-model="state.name">
                </div>
                <br>
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" class="form-control" placeholder="Username" v-model="state.username">
                </div>
                <br>
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" class="form-control" placeholder="Password" v-model="state.password">
                </div>
                <br>
                <div class="d-grid gap-2 ">
                    <button class="btn btn-primary" type="submit">Sign Up</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { reactive } from 'vue';

export default {
    name: "RegisterComponent",
    setup() {
        const state = reactive({
            name: '',
            username: '',
            password: '',
        });


        function submitHandler() { }

        return {
            state,
            submitHandler
        };
    }
}
</script>

<style scoped>
@import "@/static/css/common.css";

.card {
    border: none;
}
</style>