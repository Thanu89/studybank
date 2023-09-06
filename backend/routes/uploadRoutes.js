// import express from 'express';
// import multer from 'multer';
// import { v2 as cloudinary } from 'cloudinary';
// import streamifier from 'streamifier';
// import { isAuth } from './utils.js;';

// const upload = multer();

// const uploadRouter = express.Router();

// uploadRouter.post(
//   '/',
//   isAuth,
//   isAdmin,
//   upload.single('source_file'),
//   async (req, res) => {
//     cloudinary.config({
//       cloud_name: process.env.CLOUDINARY,
//       api_key: process.env.CLOUDINARY_API,
//       api_secret: process.env.CLOUDINARY_SECRET,
//     });
//     const streamUpload = (req) => {
//       return new Promise((resolve, reject) => {
//         const stream = cloudinary.uploader.upload_stream((error, result) => {
//           if (result) {
//             resolve(result);
//           } else {
//             reject(error);
//           }
//         });
//         streamifier.createReadStream(req.file.buffer).pipe(stream);
//       });
//     };
//     const result = await streamUpload(req);
//     res.send(result);
//   }
// );
// uploadRouter.post(
//   '/',
//   isAuth,
//   isAdmin,
//   upload.single('target_file'),
//   async (req, res) => {
//     cloudinary.config({
//       cloud_name: process.env.CLOUDINARY,
//       api_key: process.env.CLOUDINARY_API,
//       api_secret: process.env.CLOUDINARY_SECRET,
//     });
//     const streamUpload = (req) => {
//       return new Promise((resolve, reject) => {
//         const stream = cloudinary.uploader.upload_stream((error, result) => {
//           if (result) {
//             resolve(result);
//           } else {
//             reject(error);
//           }
//         });
//         streamifier.createReadStream(req.file.buffer).pipe(stream);
//       });
//     };
//     const result = await streamUpload(req);
//     res.send(result);
//   }
// );
// export default uploadRouter;
