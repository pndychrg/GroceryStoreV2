<template>
    <div>
        <h1>Manager Dashboard</h1>
    </div>
</template>

<script>
import { reportMethods } from '@/services/HTTPRequests/reportMethods';
import { onMounted } from 'vue';
export default {
    name: "ManagerDashboard",
    setup() {
        onMounted(async () => {
            await reportMethods.downloadReportCSV()
        })
    }
}
</script>

<style scoped></style>