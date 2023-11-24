<template>
    <div class="rating-card">
        <div class="card-body text-start">
            <div class="row">
                <h5 class="card-title col-md-6">Product</h5>
                <p class="product-details col-md-6 text-end">
                    {{ rating.product.name }}
                    <br>
                    <span class="text-secondary">
                        {{ rating.product.section.name }}
                    </span>
                </p>
            </div>
            <hr>
            <div class="row">
                <h5 class="card-title col-md-6" style="align-self: center;">Rating</h5>
                <RenderStarRating :avgRating="rating.rating" class="col-md-6" style="justify-content: end;" />
            </div>
            <hr>
            <div class="row">
                <h5 class="card-title col-md-6">Comment</h5>
                <p class="col-md-6">{{ rating.comment }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import RenderStarRating from "@/components/widgets/render_star_rating.vue"
export default {
    name: "ProductRatingCard",
    components: {
        RenderStarRating
    },
    props: {
        rating: {
            type: Object,
            required: true
        }
    }
}
</script>

<style scoped></style>