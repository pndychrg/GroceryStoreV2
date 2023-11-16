<template>
    <div class="auth-wrapper my-4 container" style="min-height: 85vh;">
        <div class="auth-inner card">
            <form @submit.prevent="submitHandler">
                <h3>Register</h3>
                <div class="btn-group mb-2" role="group" aria-label="User Role Radio Button Group" style="width: 100%;">
                    <input type="radio" v-model="state.role" value="user" class="btn-check" name="btnradio" id="userChekced"
                        autocomplete="off" checked>
                    <label class="btn btn-outline-primary" for="userChekced" style="width: 40%;">User</label>

                    <input type="radio" class="btn-check" v-model="state.role" value="unApproved" name="btnradio"
                        id="storeManagerChecked" autocomplete="off">
                    <label class="btn btn-outline-secondary" for="storeManagerChecked" style="width: 50;">Store
                        Manager</label>
                </div>
                <br>
                <div class="form-group ">
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
                    <label for="email">Email</label>
                    <input type="email" class="form-control" placeholder="Email" v-model="state.email">
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
import { userStateStore } from '@/services/stateManager';
export default {
    name: "RegisterComponent",
    setup() {
        const store = userStateStore()

        const state = reactive({
            name: '',
            username: '',
            email: '',
            password: '',
            role: "user",

        });

        async function submitHandler() {
            console.log(state.role)
            await store.registerUser(state.name, state.username, state.email, state.password, state.role,)
        }

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