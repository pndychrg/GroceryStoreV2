<template>
    <div class="admin-dashboard">
        <h3>Sections Page</h3>
        <div class=" row m-2 border-dark-subtle sections-wrapper border-2 border">
            <!-- TODO check here why row is used -->
            <div class="row">
                <h2 class="col text-start">
                    Sections
                    <button @click="showAddSectionForm" class="btn btn-primary btn-addSection" type="button">
                        Add Section
                    </button>
                </h2>
            </div>

            <div v-for="section in sections" :key="section.id" class="SectionCard card"
                :class="{ emtpySectionCard: section.numOfProducts == 0 }">
                <SectionCard :sectionData="section" @deleteSection="showDelete(section, 'section')"
                    @editSection="showEditSectionForm(section, 'section')" />
            </div>
            <div v-if="sections.length == 0">
                <h5>No Registered Sections Found</h5>
            </div>
        </div>

        <div class="row m-2 border-dark-subtle sections-wrapper border border-2">
            <h2 class="text-start">
                Section Requests
            </h2>
            <div v-for="section in sectionRequests" :key="section.id" class="SectionCard card">
                <SectionRequestCard :sectionRequestData="section"
                    @deleteSectionRequest="showDelete(section, 'sectionRequest')"
                    @editSectionRequest="showEditSectionForm(section, 'sectionRequest')"
                    @sectionrequest-approved="handleApprovedSection" @sectionrequest-rejected="handleRejectedSection" />
            </div>

            <div v-if="sectionRequests.length == 0">
                <h5>No Registered Sections Found</h5>
            </div>
        </div>

        <teleport to="#modal-root">
            <ConfirmationModal v-show="isDeleteModalShown" deleteElement="Section" :element="selectedSection"
                @close="isDeleteModalShown = false" @confirm="deleteSection" />
            <SectionForm v-show="isSectionFormShown" :initialData="selectedSection" :itemType="itemType" @close="formClosed"
                @section-added="handleAddSectionEvent" @section-edited="handleEditSectionEvent"
                @sectionRequest-edited="handleEditSectionRequestEvent" />
        </teleport>
    </div>
</template>

<script>
import ConfirmationModal from '@/components/widgets/confirmation.vue'
import SectionForm from '@/components/widgets/forms/section_form.vue'
import { userStateStore } from '@/services/stateManager';
import { onMounted, ref } from 'vue';
import { sectionMethods } from '@/services/HTTPRequests/sectionMethods'
import SectionCard from '@/components/widgets/cards/section_card.vue';
import SectionRequestCard from '@/components/widgets/cards/section_request_card.vue'
export default {
    name: 'SectionsPage',
    components: {
        SectionCard,
        SectionForm,
        ConfirmationModal,
        SectionRequestCard,
    },
    setup() {
        const store = userStateStore()
        const sections = ref([]);
        const sectionRequests = ref([]);
        const selectedSection = ref(null);
        const itemType = ref("section");
        const isSectionFormShown = ref(false);
        const showAddSectionForm = () => {
            isSectionFormShown.value = true
        }
        const showEditSectionForm = (section, item) => {
            isSectionFormShown.value = true
            selectedSection.value = section
            itemType.value = item
        }

        const handleEditSectionRequestEvent = (editedSectionRequest) => {
            sectionRequests.value.map((section, index) => {
                if (section.id == editedSectionRequest?.id) {
                    sectionRequests.value[index] = editedSectionRequest
                }
            });
            formClosed()
        }

        const handleApprovedSection = (approvedSection, sectionRequestData) => {
            if (sectionRequestData.request == 'add') {
                sections.value.unshift(approvedSection);
            }
            else if (sectionRequestData.request == 'edit') {
                sections.value.map((section, index) => {
                    if (section.id == approvedSection?.id) {
                        sections.value[index] = approvedSection

                    }
                })
            }
            else {
                sections.value = sections.value.filter(s => s.id !== sectionRequestData.reg_section_id);
            }
            // removing the section requeset from section request list
            sectionRequests.value = sectionRequests.value.filter(s => s !== sectionRequestData);

        }
        const handleRejectedSection = (response, sectionRequestData) => {
            // if the response is true
            // delete the section request
            if (response) {
                sectionRequests.value = sectionRequests.value.filter(s => s !== sectionRequestData);
            }
        }
        const formClosed = () => {
            isSectionFormShown.value = false
            selectedSection.value = null
        }
        const handleAddSectionEvent = (newSection) => {
            if (store.user.role == 'admin') {
                sections.value.unshift(newSection);
                isSectionFormShown.value = false
                selectedSection.value = null
            } else {
                sectionRequests.value.unshift(newSection);
                isSectionFormShown.value = false;
                selectedSection.value = null
            }
        }
        const handleEditSectionEvent = (editedSection) => {
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
        const showDelete = (sectionData, item) => {
            selectedSection.value = sectionData
            itemType.value = item
            isDeleteModalShown.value = true
            console.log("From dashboard", sectionData);
        }

        const deleteSection = async (section) => {
            if (itemType.value === 'section') {
                try {
                    const response = await sectionMethods.deleteSection(section);
                    if (response && store.user.role == 'admin') {
                        sections.value = sections.value.filter(s => s !== section);
                    } else if (response && store.user.role == 'manager') {
                        sectionRequests.value.unshift(response);
                    }

                } catch (e) {
                    console.log(e)
                }
            } else {
                const response = await sectionMethods.deleteSectionRequest(
                    section.id
                );
                if (response) {
                    sectionRequests.value = sectionRequests.value.filter(s => s !== section);
                }
            }
        }
        const fetchSectionsData = async () => {
            try {
                const sectionsData = await sectionMethods.fetchAllSections();
                sections.value = sectionsData;
                sectionRequests.value = await sectionMethods.fetchAllSectionRequests()
            } catch (e) {
                console.error('Error fetching sections', e);
            }
        }
        onMounted(() => {
            fetchSectionsData();

        })
        return {
            sections,
            sectionRequests,
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
            handleApprovedSection,
            handleEditSectionRequestEvent,
            handleRejectedSection,
            itemType,
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

.emtpySectionCard {
    box-shadow: rgba(235, 19, 19, 0.2) 0px 7px 29px 0px;
}

.btn-addSection {
    background-color: #4D6DE3;
}
</style>