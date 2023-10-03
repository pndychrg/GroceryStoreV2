<template>
    <div class="card section-card">
        <div class="card-body text-start">
            <h5 class="card-title ">{{ sectionData.name }}</h5>
            <h6 class="card-text text-secondary">Unit - {{ sectionData.unit }}</h6>
        </div>
    </div>
</template>

<script>
export default {
    name: "SectionCard",
    props: {
        sectionData: Object,
    },
    // setup(props,{emit}){

    // }
}
</script>

<style  scoped>
.section-card {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    width: 18rem;
    margin: 10px;
}
</style>