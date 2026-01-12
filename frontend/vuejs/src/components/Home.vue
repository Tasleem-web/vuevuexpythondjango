<template>
  <div class="home">
    <a-row :gutter="[16, 16]">
      <a-col :xs="24" :sm="24" :md="12" :lg="12">
        <a-card :title="isEditing ? 'Edit Member' : 'Add Member'" :bordered="false">
          <a-form 
            layout="vertical" 
            @finish="onSubmitForm"
            :model="form"
            ref="formRef"
          >
            <a-form-item label="Name" name="name" :rules="[{ required: true, message: 'Please enter name' }]">
              <a-input v-model:value="form.name" placeholder="Enter name" />
            </a-form-item>
            <a-form-item label="Email" name="email" :rules="[{ required: true, type: 'email', message: 'Please enter valid email' }]">
              <a-input v-model:value="form.email" placeholder="Enter email" type="email" />
            </a-form-item>
            <a-form-item label="Status" name="status" :rules="[{ required: true, message: 'Please select status' }]">
              <a-select 
                v-model:value="form.status" 
                placeholder="Select status"
                allow-clear
              >
                <a-select-option 
                  v-for="lookup in lookUpData" 
                  :key="lookup.status_id"
                  :value="lookup.status_id"
                >
                  {{ lookup.status }}
                </a-select-option>
              </a-select>
            </a-form-item>
            <a-form-item>
              <a-space>
                <a-button type="primary" html-type="submit" :loading="loading">
                  {{ isEditing ? 'Update Member' : 'Add Member' }}
                </a-button>
                <a-button v-if="isEditing" @click="cancelEdit">Cancel</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>

      <a-col :xs="24" :sm="24" :md="12" :lg="12">
        <a-card title="Statistics" :bordered="false">
          <a-row :gutter="16">
            <a-col :xs="12" :sm="12" :md="8" :lg="8">
              <a-statistic title="Total Members" :value="memberCount" />
            </a-col>
            <a-col :xs="12" :sm="12" :md="8" :lg="8">
              <a-statistic title="Active Members" :value="activeMemberCount" />
            </a-col>
            <a-col :xs="12" :sm="12" :md="8" :lg="8">
              <a-button type="primary" @click="fetchMembers" :loading="loading">
                Refresh
              </a-button>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-divider />

    <a-card title="Members List" :bordered="false">
      <a-alert
        v-if="error"
        message="Error"
        :description="error"
        type="error"
        show-icon
        closable
        style="margin-bottom: 16px"
      />
      
      <a-spin :spinning="loading">
        <a-table
          :columns="columns"
          :data-source="members"
          row-key="id"
          :pagination="{ pageSize: 10 }"
          :scroll="{ x: 800 }"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'status'">
              <a-tag :color="getStatusColor(record.status)">
                {{ record.status }}
              </a-tag>
            </template>
            <template v-else-if="column.key === 'action'">
              <a-space>
                <a-button type="link" size="small" @click="editMember(record)">Edit</a-button>
                <a-button type="link" danger size="small" @click="deleteMember(record.id)">Delete</a-button>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-spin>
    </a-card>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Home',
  data() {
    return {
      form: {
        id: null,
        name: '',
        email: '',
        status: undefined
      },
      isEditing: false,
      columns: [
        {
          title: 'ID',
          dataIndex: 'id',
          key: 'id',
          width: 80
        },
        {
          title: 'Name',
          dataIndex: 'name',
          key: 'name',
          width: 150
        },
        {
          title: 'Email',
          dataIndex: 'email',
          key: 'email',
          width: 200
        },
        {
          title: 'Status',
          dataIndex: 'status',
          key: 'status',
          width: 120
        },
        {
          title: 'Created At',
          dataIndex: 'created_at',
          key: 'created_at',
          width: 180
        },
        {
          title: 'Action',
          key: 'action',
          width: 120,
          fixed: 'right'
        }
      ]
    }
  },
  computed: {
    ...mapState(['members', 'loading', 'error', 'lookUpData']),
    memberCount() {
      return this.members.length
    },
    activeMemberCount() {
      return this.members.filter(m => m.status === 'active').length
    }
  },
  methods: {
    ...mapActions(['fetchMembers', 'addMember', 'fetchLookUp']),
    async onSubmitForm() {
      try {
        if (this.isEditing) {
          await this.onUpdateMember()
        } else {
          await this.onAddMember()
        }
      } catch (error) {
        this.$message.error('Operation failed')
      }
    },
    async onAddMember() {
      try {
        await this.addMember(this.form)
        this.$message.success('Member added successfully!')
        this.form = { id: null, name: '', email: '', status: undefined }
        await this.fetchMembers()
      } catch (error) {
        this.$message.error('Failed to add member')
        console.error(error)
      }
    },
    editMember(record) {
      const statusId = this.lookUpData.find(l => l.status_id === +record.status)?.status_id
      Object.assign(this.form, {
        id: record.id,
        name: record.name,
        email: record.email,
        status: statusId
      })
      this.isEditing = true
    },
    async onUpdateMember() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/partialUpdateMember/${this.form.id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.form.name,
            email: this.form.email,
            status: this.form.status
          })
        })
        if (!response.ok) throw new Error('Failed to update')
        this.$message.success('Member updated successfully!')
        this.cancelEdit()
        await this.fetchMembers()
      } catch (error) {
        this.$message.error('Failed to update member')
        console.error(error)
      }
    },
    cancelEdit() {
      this.isEditing = false
      this.form = { id: null, name: '', email: '', status: undefined }
    },
    async deleteMember(id) {
      this.$confirm({
        title: 'Confirm Delete',
        content: 'Are you sure you want to delete this member?',
        okText: 'Yes',
        cancelText: 'No',
        onOk: async () => {
          try {
            await fetch(`http://127.0.0.1:8000/api/deleteMember/${id}`, { method: 'DELETE' })
            this.$message.success('Member deleted successfully!')
            await this.fetchMembers()
          } catch (error) {
            this.$message.error('Failed to delete member')
          }
        }
      })
    },
    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString()
    },
    getStatusColor(status) {
      const colors = {
        active: 'green',
        inactive: 'red',
        pending: 'orange'
      }
      return colors[status] || 'blue'
    }
  },
  mounted() {
    this.fetchMembers();
    this.fetchLookUp();
  }
}
</script>

<style scoped>
.home {
  width: 100%;
}
</style>
