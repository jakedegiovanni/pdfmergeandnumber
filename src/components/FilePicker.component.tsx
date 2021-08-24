import React, { ChangeEvent, MouseEvent, useState } from 'react';
import FileViewer, { FileRepresentation } from './FileViewer.componet';

// const PDFDocument = require('pdfkit');
// const blobStream = require('blob-stream');

const isDefined = (x: any) => x !== null && x !== undefined;

type FileMapping = {[name: string]: FileRepresentation};

const FilePicker = () => {

    // const doc = new PDFDocument();
    // const stream = doc.pipe(blobStream());
    // doc.end();
    // stream.on('finish', () => {
    //     const blob = stream.toBlob('aplication/pdf');
    //     console.log(blob);
    //     console.log(stream.toBlobURL('application/pdf'));
    // });

    const [files, setFiles] = useState<FileMapping>({});

    const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
        const files1 = e.target.files;
        if (!isDefined(files1)) return;

        const promises: Promise<FileRepresentation>[] = [];
        for (let i = 0; i < files1!.length; i++) {
            const p = new Promise<FileRepresentation>(((resolve, reject) => {
                const fr = new FileReader();
                fr.readAsDataURL(files1![i]);
                fr.onload = e => {
                    const dataUrl: string = e.target!.result as string;
                    const file = files1![i];
                    // todo: get redux pulled in
                    resolve({file, dataUrl});
                };
                fr.onerror = e => {
                    reject(fr.error);
                    // todo
                };
            }));
            promises.push(p);
        }
        Promise.allSettled(promises)
            .then((r: PromiseSettledResult<FileRepresentation>[]) => {
                const newFiles = {...files};
                r.forEach(s => {
                    if (s.status === 'fulfilled') {
                        const dataUrl: string = s.value.dataUrl;
                        const file = s.value.file;
                        const name: string = s.value.file.name;
                        newFiles[name] = {file, dataUrl};
                    } else if (s.status === 'rejected') {
                        // todo: handle rejected files better
                        console.warn(s.reason);
                    }
                });
                setFiles(newFiles);
            });
    };

    const uploadFiles = (e: MouseEvent<HTMLButtonElement>) => {};

    return (
        <div>
            <input type="file" name="files" multiple onChange={changeHandler} />
            <button onClick={uploadFiles}>Upload</button>

            {
                Object.values(files).map((f) =>
                    <FileViewer key={f.file.name} r={f} />)
            }
        </div>
    );
};

export default FilePicker;