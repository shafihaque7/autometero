<template>
  <Transition name="fade" mode="out-in">
    <slot></slot>
  </Transition>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.0s ease-in;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
