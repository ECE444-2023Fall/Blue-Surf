import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { faPlus, faXmark } from "@fortawesome/free-solid-svg-icons";
import { Dropdown } from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "font-awesome/css/font-awesome.min.css";
import "../styles/PostDetailsPage.css";
import AutoSizeTextArea from "./AutoSizeTextArea";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Post {
  title: string;
  start_time: Date;
  location: string;
  description: string;
  extended_description: string;
  tags: string[];
  id: number;
  author_id: number;
  is_published: boolean;
  end_time: Date;
  like_count: number;
  club?: string;
  image?: Blob;
}

const PostDetailsPage: React.FC = () => {
  const { postId } = useParams();

  const [post, setPost] = useState<Post | null>(null);
  const [editedPost, setEditedPost] = useState<Post | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [imageSrc, setImageSrc] = useState<string | ArrayBuffer | undefined>(undefined);
  const [tags, setTags] = useState<string[]>([]);

  const getTagNames = async (): Promise<any[] | null> => {
    try {
      const response = await fetch("/api/get-all-tags");
      if (response.ok) {
        const data = await response.json();
        return data;
      } else {
        console.error("Failed to fetch all tag names");
        return null;
      }
    } catch (error) {
      console.error("Error fetching tag names:", error);
      return null;
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      const tags = await getTagNames();
      if (tags) {
        setTags(tags);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`/api/${postId}`);
        if (!response || !response.ok) {
          throw new Error("Cannot fetch post.");
        }
        const data: Post = await response.json();
        setPost(data);
        setEditedPost({ ...data, image: undefined }); // Set image to undefined initially
        setImageSrc(data.image ? URL.createObjectURL(data.image) : undefined);
      } catch (error) {
        console.error("Error fetching post:", error);
      }
    };

    fetchData();
  }, [postId]);

  if (!post || !editedPost) {
    return <div>Loading...</div>;
  }

  const toggleEdit = () => {
    if (isEditing) {
      setEditedPost({ ...post, image: undefined });
    }
    setIsEditing(!isEditing);
  };

  const handleSave = async () => {
    try {
      const response = await fetch(`/api/update-post/${postId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(editedPost),
      });

      if (response.ok) {
        setIsEditing(false);
        setPost({ ...editedPost });
      } else {
        console.error("Failed to update post.");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleCancel = () => {
    setEditedPost({ ...post, image: undefined });
    setIsEditing(false);
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files && event.target.files[0];

    if (selectedFile) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const newImageSrc = e.target && e.target.result;

        if (newImageSrc instanceof Blob) {
          setImageSrc(URL.createObjectURL(newImageSrc));
          setEditedPost({ ...editedPost!, image: newImageSrc });
        } else if (typeof newImageSrc === 'string') {
          setImageSrc(newImageSrc);
        }
      };

      reader.readAsDataURL(selectedFile);
    }
  };

  // ... (rest of the component)

  return (
    <div className="post-details-wrapper">
      {/* ... (rest of the component) */}
    </div>
  );
};

export default PostDetailsPage;
