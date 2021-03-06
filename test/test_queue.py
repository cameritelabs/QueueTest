import unittest
import time

from src.queue import DeleteAttemptToUnknownMessage, Queue, Full, RepeatedMessage, Empty


class TestQueue(unittest.TestCase):
    def setUp(self):
        pass

    def test_put(self):
        queue = Queue(maxsize=1)

        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        with self.assertRaises(Full):
            queue.put("2.txt", {"content": "file content"}, timeout=1)

        queue = Queue(maxsize=1)

        with self.assertRaises(ValueError):
            queue.put("1.txt", {"content": "file content"}, timeout=-4)

        queue = Queue(maxsize=2)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"content": "file content"}, timeout=1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

        with self.assertRaises(RepeatedMessage):
            queue.put("1.txt", {"content": "file content"}, timeout=1)

        queue = Queue(maxsize=0)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)
        queue.put("1.txt", {"content": "file content"}, timeout=1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

    def test_get(self):
        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        with self.assertRaises(Empty):
            queue.get(timeout=1)

        with self.assertRaises(ValueError):
            queue.get(timeout=-4)

        queue.put("1.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        queue_message = queue.get(timeout=1)
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue = Queue(maxsize=2)

        queue.put("1.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

        queue_message = queue.get()
        self.assertEqual(queue_message.id, "1.txt")
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), False)

        queue.put("2.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 2)
        self.assertEqual(queue.full(), True)

        queue_message = queue.get()
        self.assertEqual(queue_message.id, "2.txt")
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue.qsize(), 2)
        self.assertEqual(queue.full(), True)

    def test_acquire_timeout(self):
        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        queue.put("1.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue_message = queue.get(timeout=1, acquire_timeout=0.1)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue_message.id, "1.txt")

        time.sleep(0.5)

        queue_message = queue.get(timeout=1, acquire_timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue_message.id, "1.txt")

        with self.assertRaises(Empty):
            queue_message = queue.get(timeout=1, acquire_timeout=10)

    def test_delete(self):
        queue = Queue(maxsize=1)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        queue.put("1.txt", {"content": "file content"}, timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        queue_message = queue.get(timeout=1, acquire_timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)
        self.assertEqual(queue_message.content, {"content": "file content"})
        self.assertEqual(queue_message.id, "1.txt")

        queue.delete(queue_message.id)
        self.assertEqual(queue.qsize(), 0)
        self.assertEqual(queue.full(), False)

        queue.put("1.txt", {"content": "file content"}, timeout=10)
        queue_message = queue.get(timeout=1, acquire_timeout=10)
        self.assertEqual(queue.qsize(), 1)
        self.assertEqual(queue.full(), True)

        with self.assertRaises(DeleteAttemptToUnknownMessage):
            queue.delete("random_file.txt")

    def tearDown(self):
        pass
