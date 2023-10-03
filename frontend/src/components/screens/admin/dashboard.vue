<template>
    <div class="admin-dashboard">
        <h3>Admin Dashboard</h3>
        <div class=" row m-2 border-dark-subtle sections-wrapper border-2 border">
            <div class="row">
                <h2 class="col text-start">
                    Sections
                    <button @click="showAddSectionForm" class="btn btn-primary btn-addSection" type="button"
                        data-bs-toggle="modal" data-bs-target="#sectionForm" id="addSectionBtn">
                        Add Section
                    </button>
                </h2>
            </div>
            <div v-for="section in sections" :key="section.id">
                <SectionCard :sectionData="section" />
            </div>


            <!-- Form Section -->
            <div class="modal fade" id="sectionForm" tabindex="-1" aria-labelledby="sectionForm" aria-hidden="false">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <SectionForm v-if="isAddingSection" formTitle="Add Section" submitButtonText="Submit"
                            @cancel="hideForm" @section-added="handleSectionAdded" />
                        <SectionForm v-else formTitle="Edit Section" submitButtonText="Update"
                            :initialData="selectedSection" @cancel="hideForm" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SectionForm from '@/components/widgets/forms/section_form.vue'
import { onMounted, ref } from 'vue';
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods'
import SectionCard from '@/components/widgets/section_card.vue';
export default {
    name: 'AdminDashboard',
    components: {
        SectionCard,
        SectionForm,

    },
    setup() {
        const sections = ref([]);
        const isFormVisible = ref(false);
        const selectedSection = ref(null);
        const isAddingSection = ref(true);

        // function to set the boolean values 
        const showAddSectionForm = () => {
            isAddingSection.value = true;
            selectedSection.value = null;
            isFormVisible.value = true;

        }

        const showEditSectionForm = (section) => {
            isAddingSection.value = false;
            selectedSection.value = section;
            isFormVisible.value = true
        }

        const hideForm = () => {
            isFormVisible.value = false
            document.getElementById('addSectionBtn').click();
        }

        const handleSectionAdded = (newSection) => {
            // console.log(newSection)
            sections.value.push(newSection);
            hideForm();
        }

        const fetchSectionsData = async () => {
            try {
                const sectionsData = await sectionMethods.fetchAllSections();
                sections.value = sectionsData;
            } catch (e) {
                console.error('Error fetching sections', e);
            }
        }
        onMounted(() => {
            fetchSectionsData();

        })

        return {
            sections,
            showAddSectionForm,
            showEditSectionForm,
            hideForm,
            isFormVisible,
            isAddingSection,
            selectedSection,
            handleSectionAdded,
        }
    }
}
</script>

<style scoped>
.sections-wrapper {
    margin: auto;
    background-color: #ffffff;
    /* box-shadow: 0px 14px 80px rgba(34, 35, 58, 0.2); */
    padding: 40px 55px 45px 55px;
    border-radius: 15px;
    transition: all .3s;
}


.btn-addSection {
    background-color: #4D6DE3;
}
</style>