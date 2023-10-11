<template>
    <div class="section-card">
        <div class="card-body text-start">
            <h5 class="card-title">{{ sectionRequestData.name }}
                <!-- Add Badge -->
                <span class="badge text-bg-primary rounded-pill float-end " v-if="sectionRequestData.request === 'add'">{{
                    sectionRequestData.request }}</span>
                <!-- Edit Badge -->
                <span class="badge text-bg-warning rounded-pill float-end" v-if="sectionRequestData.request === 'edit'">{{
                    sectionRequestData.request
                }}</span>

                <!-- Delete Badge -->
                <span class="badge text-bg-danger rounded-pill float-end" v-if="sectionRequestData.request === 'delete'">{{
                    sectionRequestData.request }}</span>
            </h5>

            <h6 class="card-text text-secondary">{{ sectionRequestData.unit }} </h6>
            <!-- buttons different for manager and admin -->
            <hr>

            <div v-if="user.role == 'admin'" class="d-flex justify-content-end">
                <button class="btn" @click="handleRejection">
                    <font-awesome-icon :icon="['fas', 'xmark']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn " @click="handleApproval">
                    <font-awesome-icon :icon="['fas', 'check']" class="faa-horizontal animated-hover"
                        style="color: green;" />
                </button>
            </div>
            <div v-else class="d-flex justify-content-end">
                <button class="btn" @click="$emit('deleteSectionRequest')">
                    <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn" @click="$emit('editSectionRequest')">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { userStateStore } from '@/services/stateManager';
// import { computed } from 'vue';
import { sectionRequestMethodsForAdmin } from '@/services/HTTPRequests/section_approval';
export default {
    name: "SectionRequestCard",
    props: {
        sectionRequestData: Object
    },
    setup(props, { emit }) {
        const store = userStateStore();

        // handling editing and deleting the section request by store manager



        // handling approval and rejection from admin here
        const handleApproval = async () => {
            const response = await sectionRequestMethodsForAdmin.approveSectionRequest(props.sectionRequestData.id);
            if (response) {
                console.log(response);
                emit('sectionrequest-approved', response, props.sectionRequestData);
            }
        }
        const handleRejection = async () => {
            const response = await sectionRequestMethodsForAdmin.rejectSectionRequest(props.sectionRequestData.id);
            if (response) {
                console.log(response);
                emit('sectionrequest-rejected', response, props.sectionRequestData);
            }
            console.log("rejection")
        }

        return {
            user: store.user,
            handleApproval,
            handleRejection,
        }
    }
}
</script>

<style scoped></style>