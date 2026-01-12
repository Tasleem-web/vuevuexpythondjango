import { createStore } from 'vuex'

export default createStore({
  state() {
    return {
      members: [],
      loading: false,
      error: null,
      lookUpData: []
    }
  },
  mutations: {
    setMembers(state, members) {
      state.members = members
    },
    addMember(state, member) {
      state.members.push(member)
    },
    setLoading(state, loading) {
      state.loading = loading
    },
    setError(state, error) {
      state.error = error
    },
    setLookUp(state, lookUpData) {
      state.lookUpData = lookUpData
    }
  },
  actions: {
    async fetchMembers({ commit }) {
      commit('setLoading', true)
      try {
        const response = await fetch('http://127.0.0.1:8000/api/getMembers/')
        const data = await response.json()
        commit('setMembers', data)
        commit('setError', null)
      } catch (error) {
        commit('setError', error.message)
      } finally {
        commit('setLoading', false)
      }
    },
    async fetchLookUp({ commit }) {
      commit('setLoading', true)
      try {
        const response = await fetch('http://127.0.0.1:8000/api/getLookUp/')
        const data = await response.json()
        commit('setLookUp', data)
        commit('setError', null)
        return data
      } catch (error) {
        commit('setError', error.message)
        throw error
      } finally {
        commit('setLoading', false)
      }
    },

    async addMember({ commit }, member) {
      commit('setLoading', true)
      try {
        const response = await fetch('http://127.0.0.1:8000/api/members/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(member)
        })
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }
        const data = await response.json()
        commit('setError', null)
        return data
      } catch (error) {
        commit('setError', error.message)
        throw error
      } finally {
        commit('setLoading', false)
      }
    }
  },
  getters: {
    members: state => state.members,
    loading: state => state.loading,
    error: state => state.error
  }
})
