<template>
    <div class="modal-overlay sidebar-overlay" @click="closeSidebar($event)">
        <div class="modal-content sidebar bg-dark text-light">
            <!-- TODO add user image here -->
            <SidebarLink route='/dashboard' :tag="store.user?.name ?? ''" @close="$emit('close')" icon="user" />
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
            <div v-if="store.user?.role == 'user'">
                <SidebarLink v-for="
                    link in userLinks" :key="link.tag" :route="link.route" :tag="link.tag" :icon="link.icon"
                    :color="link.color" @close="$emit('close')" />

            </div>
            <!-- <div class="bottom-buttons"> -->
            <button @click="$emit('close')" class="btn text-start btn-danger btn-bottom">
                <font-awesome-icon :icon="['fas', 'xmark']" /> Close
            </button>
            <!-- </div> -->
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
                icon: 'puzzle-piece'
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
                icon: 'puzzle-piece'
            },
            {
                route: '/products',
                tag: "Products",
                icon: 'fa-brands fa-product-hunt'
            },
            {
                route: '/coupons',
                tag: "Coupons",
                icon: "fa-solid fa-c",
            }
        ]
        const userLinks = [
            {
                route: '/ratings',
                tag: 'Ratings',
                icon: 'fa-star',
                color: '#f8e45c'
            }
        ]

        return {
            closeSidebar,
            store,
            adminLinks,
            managerLinks,
            userLinks
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
    border-radius: 0% !important;
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.26), 0 3px 6px rgba(0, 0, 0, 0.36);

    /* border-radius: 0px 10px 10px 0px !important; */
}

.btn-bottom {
    bottom: 10px;
    position: absolute;
    width: 70%;
}

SidebarLink {
    width: 70%;
}
</style>