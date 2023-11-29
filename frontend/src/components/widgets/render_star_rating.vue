<template>
    <div class="star-rating">
        <div v-for="n in 5" :key="n">
            <font-awesome-icon v-if="n <= avgRating" :icon="['fas', 'fa-star']" style="color: gold;"
                :style="{ fontSize: iconSize }" />
            <!-- <i  class="fa fa-star gold"></i> -->
            <font-awesome-icon v-else-if="n - 0.5 <= avgRating" class="gold" :icon="['fas', 'fa-star-half-alt']"
                style="color: gold;" :style="{ fontSize: iconSize }" />
            <font-awesome-icon v-else :icon="['fas', 'fa-star']" style="color: grey;" :style="{ fontSize: iconSize }" />
        </div>
        <h6 style="align-self: center;">({{ avgRating }})</h6>
    </div>
</template>

<script>
export default {
    name: "RenderStarRating",
    props: {
        avgRating: Number,
        iconSize: String,
    }
}
</script>

<style scoped>
.star-rating {
    font-size: 2em;
    display: flex;
    flex-wrap: wrap;
}

/* font-awesome-icon {
    size: 5px;
} */
</style>