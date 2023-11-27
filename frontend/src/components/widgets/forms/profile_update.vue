<template>
    <div class="modal-overlay" @click="closeModal($event)">
        <div class="modal-content">
            <div class="modal-header">
                <h4>Profile Update</h4>
            </div>
            <div class="user-form">
                <form @submit.prevent="updateUser">
                    <div class="modal-body">
                        <div class="form-group" style="display: grid;">
                            <!-- <h6>Profile Image</h6> -->
                            <label for="img">Profile Image</label>
                            <!-- <img v-if="formData.img != null" :src="'data:image/png;base64,' + formData.img"
                                class="image img-fluid" alt=""> -->
                            <img v-if="previewImage != null" :src="previewImage" alt=""
                                class="image img-thumbnail avatar mb-2" style="justify-self: center;">
                            <img v-else src="@/assets/img_notavailable.jpeg" alt="" class="image img-thumbnail avatar mb-2"
                                aria-hidden="true" style="justify-self: center;">
                            <div class="input-group">
                                <input type="file" class="formFile form-control" @change="handleFileUpload">
                                <button v-if="previewImage != null" class="btn btn-outline-danger" @click="clearImage">
                                    <font-awesome-icon icon="fa-solid fa-xmark" /></button>
                            </div>
                        </div>
                        <div class="form-group">
                            <label for="name">Name</label>
                            <input v-model="formData.name" type="text" id="name" class="form-control mb-2" required>
                        </div>
                        <div class="form-group">
                            <label for="username">Username</label>
                            <input v-model="formData.username" type="text" id="username" class="form-control mb-2" required>
                        </div>
                        <div class="form-group">
                            <label for="email">Email</label>
                            <input v-model="formData.email" type="text" id="email" class="form-control mb-2" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Password</label>
                            <input v-model="formData.password" type="password" id="password" class="form-control mb-2"
                                required>
                        </div>
                        <button v-if="isFormUpdated == true" type="submit" class="btn btn-outline-success"
                            style="width: 100%;">Submit</button>
                        <button v-else disabled type="submit" class="btn btn-outline-success"
                            style="width: 100%;">Submit</button>
                    </div>
                </form>

            </div>
            <!-- <h1>Profile Update</h1> -->
            <!-- <p>{{ user }}</p> -->
        </div>
    </div>
</template>

<script>
import { userStateStore } from '@/services/stateManager';
import { ref, computed, watch, onMounted } from 'vue';
export default {
    name: "UserProfileUpdateForm",
    setup(props, { emit }) {
        const store = userStateStore();
        const user = store.user;
        const formData = ref({ ...user, password: null, img: null });
        // const selectedImage = ref(store.profile_img)
        // const password = ref();
        const previewImage = computed(() => {
            // console.log(`store ${store.profile_img}`)
            // console.log(`form ${formData.value.img}`)
            // formData.value.img = store.profile_img;

            // first checking if the formData got any img from user that will be in blob 
            if (formData.value.img != null) {
                if (typeof (formData.value.img) === 'string') {
                    return `data:image/png;base64,${formData.value.img}`
                } else {
                    return URL.createObjectURL(formData.value.img)
                }
            }
            return null;
            // return formData.value.img ? URL.createObjectURL(formData.value.img) : null;
        })
        const handleFileUpload = (event) => {
            formData.value.img = event.target.files[0]
            console.log(formData)
        }
        const clearImage = () => {
            formData.value.img = null;
        }
        const closeModal = ($event) => {
            // first clearing the password in formData
            // formData.value.password = null;
            if ($event != null) {
                if ($event.target.classList.contains('modal-overlay')) {
                    emit('close');
                }
            } else {
                emit('close')
            }
        }

        const updateUser = async () => {
            const data = {
                ...formData.value,
                // password: password.value,
            }
            console.log(data);
            // const imgData = new FormData();
            // imgData.append("image", formData.value.img)
            // update the image first so then in jwt token we will get the img back
            const response = await store.updateUser(data);
            // console.log(response)
            if (response) {
                await store.setUserImage(formData.value.img);
            } else {
                // emtying the formData and refilling it with userData
                formData.value = { ...user, password: null, img: null }
            }
            formData.value.password = null;
            // console.log(response)
            closeModal();
            // emit("user-updated");
        }
        const isFormUpdated = ref(false);
        watch(formData.value, () => {
            isFormUpdated.value = true;
        }, { deep: true });

        onMounted(async () => {
            if (store.profile_img === null) {
                // image fetched
                await store.getUserImage();
                formData.value.img = store.profile_img
                // console.log(formData.value.img)
            } else {
                formData.value.img = store.profile_img
            }
        })

        return {
            user,
            closeModal,
            formData,
            // password,
            previewImage,
            clearImage,
            isFormUpdated,
            handleFileUpload,
            updateUser

        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";

.modal-content {
    width: 80%;
}

.image {
    height: 20vh !important;
}
</style>