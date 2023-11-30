<template>
    <div class="modal-overlay" @click="closeModal($event)">
        <div class="modal-content">
            <div class="modal-header">
                <h4>Update Passowrd</h4>
            </div>
            <div class="modal-boy">
                <div class="form-wrapper">
                    <form @submit.prevent="updatePassword">
                        <!-- Old Password -->
                        <div class="mb-3">
                            <label for="oldPassword" class="form-label">Old Password</label>
                            <input type="password" class="form-control" id="oldPassword" name="oldPassword" required
                                v-model="formData.current_password">
                        </div>

                        <!-- New Password -->
                        <div class="mb-3">
                            <label for="newPassword" class="form-label">New Password</label>
                            <input type="password" class="form-control" id="newPassword" name="newPassword" required
                                v-model="formData.new_password">
                        </div>

                        <!-- Confirm New Password -->
                        <div class="mb-3 ">
                            <label for="confirmPassword" class="form-label">Confirm New Password</label>
                            <input type="password" class="form-control" id="confirmPassword" name="confirmPassword" required
                                v-model="formData.confirm_password" :class="{ 'is-invalid': !arePasswordMatching }">
                            <div class="invalid-feedback ">
                                New Password is not matching
                            </div>
                        </div>

                        <div>
                            <!-- Submit Button -->
                            <button type="submit" class="btn btn-primary m-2 float-end" style="width: 30%;">Update
                                Password</button>
                            <button type="button" class="btn btn-outline-secondary m-2 float-end" style="width: 20%;"
                                @click="closeModal()">Cancel</button>
                            <button type="button" class="btn btn-outline-danger m-2 " @click="forgotPassword">
                                Forgot Password
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { computed, ref } from 'vue';
import { userStateStore } from "@/services/stateManager"
export default {
    name: "UpdatePasswordForm",
    setup(props, { emit }) {
        const store = userStateStore();
        const formData = ref({
            current_password: null,
            new_password: null,
            confirm_password: null
        })
        const arePasswordMatching = computed(() => {
            if (formData.value.new_password === null || formData.value.confirm_password === null) {
                return true;
            }
            if (formData.value.new_password === formData.value.confirm_password) {
                return true;
            } else {
                return false;
            }
        })

        // eslint-disable-next-line no-unused-vars
        const clearForm = () => {
            Object.assign(formData.value, {
                current_password: null,
                new_password: null,
                confirm_password: null
            })
        }

        const updatePassword = async () => {
            console.log("Udpate password ran")
            const data = {
                "current_password": formData.value.current_password,
                "new_password": formData.value.new_password,
            }
            const response = await store.updateUserPassword(data);
            console.log(response)
            if (response) {
                closeModal();
            }
        }

        const forgotPassword = async () => {
            const response = await store.forgotPassword()
            if (response) {
                closeModal();
            }
        }

        const closeModal = ($event) => {
            // formData.value.password = null;
            if ($event != null) {
                if ($event.target.classList.contains('modal-overlay')) {
                    emit('close');
                    clearForm()
                }
            } else {
                console.log("Close button pressed")
                emit('close')
                clearForm()
            }
        }


        return {
            closeModal,
            formData,
            arePasswordMatching,
            updatePassword,
            forgotPassword,
        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";

.modal-content {
    width: 60%;
}
</style>