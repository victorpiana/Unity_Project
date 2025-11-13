using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(Rigidbody))]
public class GrabbableBehavior : MonoBehaviour
{
    public enum GrabType { None, Free, Snap };
    public GrabType grabType = GrabType.Free;

    private Rigidbody rb;
    private GameObject grabber;
    public bool isHeld = false;
    private bool wasKinematic;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
        wasKinematic = rb.isKinematic;
    }

    public void TryGrab(GameObject newGrabber)
    {
        if (isHeld) return;

        grabber = newGrabber;
        rb.isKinematic = true;
        transform.parent = grabber.transform;
        isHeld = true;

        if (grabType == GrabType.Snap)
        {
            transform.position = grabber.transform.position;
            transform.rotation = grabber.transform.rotation;
        }
    }

    public void TryRelease(GameObject currentGrabber)
    {
        if (!isHeld || grabber != currentGrabber) return;

        transform.parent = null;
        rb.isKinematic = wasKinematic;
        grabber = null;
        isHeld = false;
    }
    public bool IsHeld()
{
    return isHeld;
}
}
