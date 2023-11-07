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
            <div v-if="store.user?.role == 'admin'">
                <SidebarLink v-for="link in adminLinks" :key="link" :route="link.route" :tag="link.tag" :icon="link.icon"
                    @close="$emit('close')" />
            </div>
            <div v-if="store.user?.role == 'manager'">
                <SidebarLink v-for="link in managerLinks" :key="link" :route="link.route" :tag="link.tag" :icon="link.icon"
                    @close="$emit('close')" />
            </div>
            <button @click="$emit('close')" class="btn text-start btn-danger ">
                <font-awesome-icon :icon="['fas', 'xmark']" /> Close
            </button>
        </div>
    </div>
</template>

<script>
import { userStateStore } from '@/services/stateManager';
import SidebarLink from './sidebar_link.vue';
// import { UIStateStore } from '@/services/uiStateManager';
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
        // const uiStore = UIStateStore();
        const closeSidebar = ($event) => {
            //clicking on the modal button through javascript
            if ($event.target.classList.contains('sidebar-overlay')) {
                emit('close');
            }
        }

        // Creating admin links here
        const adminLinks = [
            {
                route: '/sections',
                tag: "Sections",
                icon: 'arrow-right-from-bracket'
            },
            {
                route: '/admin/approveManager',
                tag: "Approve Manager",
                icon: 'arrow-right-from-bracket'
            }
        ]
        const managerLinks = [
            {
                route: '/sections',
                tag: "Sections",
                icon: 'arrow-right-from-bracket'
            },
            {
                route: '/products',
                tag: "Products",
                icon: 'arrow-right-from-bracket'
            },
            {
                route: '/coupons',
                tag: "Coupons",
                icon: "arrow-right-from-bracket",
            }
        ]

        return {
            closeSidebar,
            store,
            adminLinks,
            managerLinks
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
    height: 100%;
    width: 288px;
    margin: 0px;
    border-radius: 0px 10px 10px 0px !important;
}
</style>