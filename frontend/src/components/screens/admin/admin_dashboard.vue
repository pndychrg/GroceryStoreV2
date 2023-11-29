<template>
    <div style="display: grid;">
        <h2>Admin Dashboard</h2>
        <RouterLink to="/sections">Go To Sections Page</RouterLink>
        <div class="border border-1 border-opacity-25 rounded-2 p-4 w-75 mt-3" style="justify-self: center;">
            <h5>Admin Methods</h5>
            <ul>
                <li class="m-2">
                    <button class="btn-outline-primary btn " style="width: 100%;" @click="sendReportToAllUsers">
                        Send Report to All Users
                    </button>
                </li>
                <li class="m-2">
                    <button class="btn-outline-primary btn " style="width: 100%;" @click="sendRemainderToAllUsers">
                        Send Remainder to All Users
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import { adminMethods } from '@/services/HTTPRequests/adminMethods';
export default {
    name: "AdminDashboard",
    setup() {
        const sendReportToAllUsers = async () => {
            const response = await adminMethods.sendReportToAllUser()
            console.log(response);
        }
        const sendRemainderToAllUsers = async () => {
            const response = await adminMethods.sendRemainderToUser()
            console.log(response);
        }
        
        return {
            sendReportToAllUsers,
            sendRemainderToAllUsers
        }
    }
}
</script>

<style scoped></style>