<template>
    <div class="admin-dashboard">
        <h3>Sections Page</h3>
        <div class=" row m-2 border-dark-subtle sections-wrapper border-2 border">
            <div class="row">
                <h2 class="col text-start">
                    Sections
                    <button @click="showAddSectionForm" class="btn btn-primary btn-addSection" type="button">
                        Add Section
                    </button>
                </h2>
            </div>

            <div v-for="section in sections" :key="section.id" class="SectionCard card">
                <SectionCard :sectionData="section" @deleteSection="showDelete(section)"
                    @editSection="showEditSectionForm(section)" />
            </div>


        </div>


        <teleport to="#modal-root">
            <ConfirmationModal v-show="isDeleteModalShown" deleteElement="Section" :element="selectedSection"
                @close="isDeleteModalShown = false" @confirm="deleteSection" />
            <SectionForm v-show="isSectionFormShown" :initialData="selectedSection" @close="formClosed"
                @section-added="handleAddSectionEvent" @section-edited="handleEditSectionEvent" />
        </teleport>
    </div>
</template>

<script>
import ConfirmationModal from '@/components/widgets/confirmation.vue'
import SectionForm from '@/components/widgets/forms/section_form.vue'

import { onMounted, ref } from 'vue';
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods'
import SectionCard from '@/components/widgets/cards/section_card.vue';
export default {
    name: 'SectionsPage',
    components: {
        SectionCard,
        SectionForm,
        ConfirmationModal,
    },
    setup() {
        const sections = ref([]);
        const selectedSection = ref(null);
        // const formTitle = ref('Add Section')
        // const submitButtonText
        // add - edit section form values
        const isSectionFormShown = ref(false);
        const showAddSectionForm = () => {
            isSectionFormShown.value = true
        }
        const showEditSectionForm = (section) => {
            isSectionFormShown.value = true
            selectedSection.value = section
        }

        const formClosed = () => {
            isSectionFormShown.value = false
            selectedSection.value = null
        }

        const handleAddSectionEvent = (newSection) => {
            sections.value.unshift(newSection);
            isSectionFormShown.value = false
            selectedSection.value = null
        }

        const handleEditSectionEvent = async (editedSection) => {
            sections.value.map((section, index) => {
                if (section.id == editedSection?.id) {
                    sections.value[index] = editedSection
                }
            })
            formClosed()
            console.log("Section edited", editedSection);
        }

        // Delete Section functions and values
        const isDeleteModalShown = ref(false);
        const showDelete = (sectionData) => {
            selectedSection.value = sectionData
            isDeleteModalShown.value = true
            console.log("From dashboard", sectionData);
        }

        const deleteSection = async (section) => {
            try {
                await sectionMethods.deleteSection(section.id);

                sections.value = sections.value.filter(s => s !== section);

            } catch (e) {
                console.log(e)
            }
            console.log("section delete confirmed", section)
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
            isSectionFormShown,
            formClosed,
            handleAddSectionEvent,
            handleEditSectionEvent,
            isDeleteModalShown,
            deleteSection,
            showDelete,
            showAddSectionForm,
            showEditSectionForm,
            selectedSection,
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

    /* Flexbox settings */
    /* display: flex;
    flex-wrap: wrap;
    justify-content: space-between; */
}

.SectionCard {
    border: none;
    box-shadow: 3px 3px 5px rgba(34, 35, 58, 0.2);
    border-radius: 15px;
    transition: all .3s;
    width: 18rem;
    margin: 10px;
}

.btn-addSection {
    background-color: #4D6DE3;
}
</style>