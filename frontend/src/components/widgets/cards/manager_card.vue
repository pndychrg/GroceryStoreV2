<template>
    <div class="manager-card">
        <div class="card-body text-start">
            <h5 class="card-title">{{ managerData.name }}</h5>
            <h6 class="card-text text-secondary">{{ managerData.username }}</h6>
            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn" @click="$emit('rejected')">
                    <font-awesome-icon :icon="['fas', 'xmark']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn " @click="$emit('approved')">
                    <font-awesome-icon :icon="['fas', 'check']" class="faa-horizontal animated-hover"
                        style="color: green;" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ManagerCard",
    props: {
        managerData: Object
    }
}
</script>

<style scoped></style>