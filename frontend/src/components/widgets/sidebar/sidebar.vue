<template>
    <div class="modal-overlay sidebar-overlay" @click="closeSidebar($event)">
        <div class="modal-content sidebar">
            <!-- TODO add user image here -->
            <h2>
                <!-- TODO reroute to user dashboard by clicking on name -->
                {{ store.user?.name ?? "" }}
            </h2>
            <!-- here, three sections of buttons/tags would be present seperate for user/admin/storemanager -->
            <!-- ADMIN Sidebar -->
            <SidebarLink route="/sections" tag="Sections" icon="arrow-right-from-bracket" @close="$emit('close')" />
            <button @click="$emit('close')" class="btn text-start btn-danger ">
                <font-awesome-icon :icon="['fas', 'xmark']" /> Close
            </button>
        </div>
    </div>
</template>

<script>
import { userStateStore } from '@/services/stateManager';
import SidebarLink from './sidebar_link.vue';
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: "Sidebar",
    components: {
        SidebarLink
    },
    emits: [
        "close",
    ],
    setup(props, { emit }) {
        const store = userStateStore()
        const closeSidebar = ($event) => {
            //clicking on the modal button through javascript
            if ($event.target.classList.contains('sidebar-overlay')) {
                emit('close');
            }
        }
        return {
            closeSidebar,
            store,
        }
    }
}
</script>

<style scoped>
@import "@/static/css/modal.css";

.sidebar-overlay {
    z-index: 1031;
    justify-content: left;
    /* widows: 288px; */
}

.sidebar {
    z-index: 1032;
    position: fixed;
    top: 0;
    left: 0;
    height: 97%;
    width: 288px;
}
</style>