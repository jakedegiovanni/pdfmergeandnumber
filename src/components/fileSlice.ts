import { CaseReducer, createSlice, PayloadAction } from "@reduxjs/toolkit";

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
    const newFile: PDFFile = action.payload;
    newState[fileName] = newFile;
    state = newState;
};

export const remove: CaseReducer<State, PayloadAction<FileName>> = (state, action) => {
    const name = action.payload;
    const newState = {...state};
    delete newState[name];
    state = newState;
}

export const fileSlice = createSlice({
    name: 'files',
    initialState: {},
    reducers: {
        add, remove
    }
});

export default fileSlice.reducer;