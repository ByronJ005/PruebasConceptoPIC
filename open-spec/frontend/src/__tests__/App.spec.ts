import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'
import router from '../router'
import { createPinia } from 'pinia'

describe('App', () => {
  it('mounts successfully', () => {
    const wrapper = mount(App, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    expect(wrapper.exists()).toBe(true)
  })
})
