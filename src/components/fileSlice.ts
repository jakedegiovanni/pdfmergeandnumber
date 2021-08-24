import {CaseReducer, createSlice, PayloadAction} from "@reduxjs/toolkit";

interface PDFFile {
    f: File,
    url: string
}

type FileName = string;

interface State {
    [name: string]: PDFFile // [name: FileName]: PDFFile
}

export const add: CaseReducer<State, PayloadAction<PDFFile>> = (state, action) => {
    const newState = {...state};
    const fileName = action.payload.f.name;
    newState[fileName] = action.payload;
    state = newState;
};

export const addAll: CaseReducer<State, PayloadAction<PDFFile[]>> = (state, action) => {
    const newState = {...state};
    action.payload.forEach(pdf => newState[pdf.f.name] = pdf);
    state = newState;
};

export const remove: CaseReducer<State, PayloadAction<FileName>> = (state, action) => {
    const name = action.payload;
    const newState = {...state};
    delete newState[name];
    state = newState;
}

export const removeAll: CaseReducer<State, PayloadAction<FileName[]>> = (state, action) => {
    const newState = {...state};
    action.payload.forEach(filename => delete newState[filename]);
    state = newState;
};

export const fileSlice = createSlice({
    name: 'files',
    initialState: {},
    reducers: {
        add, addAll, remove, removeAll
    }
});

export default fileSlice.reducer;