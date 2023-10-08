<template>
    <div class="manager-card">
        <div class="card-body text-start">
            <h5 class="card-title">{{ managerData.name }}</h5>
            <h6 class="card-text text-secondary">{{ managerData.username }}</h6>
            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn">
                    <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn ">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
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