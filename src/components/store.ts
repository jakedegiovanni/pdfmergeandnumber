import { configureStore } from '@reduxjs/toolkit';
import fileSlice from './fileSlice';

const store = configureStore({
    reducer: {
        files: fileSlice
    }
});
export default store;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;