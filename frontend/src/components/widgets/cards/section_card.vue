<template>
    <div class="" :class="{}">
        <div class="card-body text-start">
            <h5 class="card-title ">{{ sectionData.name }}</h5>
            <h6 class="card-text text-secondary">
                Unit - {{ sectionData.unit }}
                <br>
                Number Of Products - <span :class="{ emptySection: sectionData.numOfProducts == 0 }">{{
                    sectionData.numOfProducts
                }}</span>
            </h6>
            <!-- <h6 class=" card-text text">
        </h6> -->
            <!-- <h6 class="card-text text-secondary" v-show="sectionData.request">{{ sectionData.request }}</h6> -->
            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn" @click="$emit('deleteSection')">
                    <font-awesome-icon :icon="['fas', 'trash-can']" class="faa-horizontal animated-hover"
                        style="color: #c01c28;" />
                </button>
                <button class="btn" @click="$emit('editSection')">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" class="faa-horizontal animated-hover" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "SectionCard",
    components: {
    },
    props: {
        sectionData: Object,
    },
}
</script>

<style  scoped>
/* .emtpy-section {} */
.emptySection {
    color: red;
    font-weight: bold;
}
</style>