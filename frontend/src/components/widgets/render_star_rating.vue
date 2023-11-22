<template>
    <div class="star-rating">
        <div v-for="n in 5" :key="n">
            <font-awesome-icon v-if="n <= avgRating" :icon="['fas', 'fa-star']" style="color: gold;" size="2xs" />
            <!-- <i  class="fa fa-star gold"></i> -->
            <font-awesome-icon v-else-if="n - 0.5 <= avgRating" class="gold" :icon="['fas', 'fa-star-half-alt']" size="2xs"
                style="color: gold;" />
            <font-awesome-icon v-else :icon="['fas', 'fa-star']" style="color: grey;" size="2xs" />
        </div>
        <h5>({{ avgRating }})</h5>
    </div>
</template>

<script>
export default {
    name: "RenderStarRating",
    props: {
        avgRating: Number,
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